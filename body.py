from datetime import datetime
import matplotlib.pyplot as plt

from data import *

crypto_reference = crypto_reference_jvm
crypto_purchases = crypto_jvm

_EPS_BTC = 1e-12


def allocate_sales(crypto_purchases, crypto_sales=None, verbose=False):
    """Match sales against purchase lots, cheapest-cost-basis-first.

    For each sale (processed in chronological order) the BTC quantity is
    consumed from purchase lots whose ``Data`` is on or before the sale date,
    selecting lots in ascending ``Preço BTC`` (ties broken by oldest purchase
    date). Sales must specify ``Reais`` and ``Preço BTC``; the BTC quantity is
    derived as ``Reais / Preço BTC``.

    Raises:
        ValueError: when the total BTC requested by sales exceeds what is
            available from eligible purchase lots.

    Returns:
        Tuple ``(lots, allocations)`` where:
            - ``lots`` is ``{purchase_id: remaining_btc}``.
            - ``allocations`` is a list of dicts, in execution order:
              ``{sale_id, sale_date, sale_datetime, sale_price,
                 purchase_id, purchase_date, purchase_datetime,
                 buy_price, btc_consumed}``.
    """
    sales = crypto_sales or {}

    lots = {}
    for purchase_id, entry in crypto_purchases.items():
        btc = entry.get("Bitcoin")
        if btc is None:
            continue
        lots[purchase_id] = btc

    allocations = []
    if verbose:
        print("Alocação de vendas (mais barato primeiro):")
        header = (f"  {'Venda':<10} {'Compra':<10} {'BTC consumido':>14} "
                  f"{'Preço compra':>14} {'Preço venda':>14} {'Retorno':>10}")
        print(header)
        print("  " + "-" * (len(header) - 2))

    sorted_sales = sorted(sales.items(), key=lambda kv: kv[1]["Data"])
    for sale_id, sale in sorted_sales:
        sale_price = sale["Preço BTC"]
        btc_to_consume = sale["Reais"] / sale_price
        sale_datetime = sale["Data"]
        sale_date = sale_datetime.strftime("%Y-%m-%d")

        eligible = []
        for purchase_id, remaining in lots.items():
            if remaining <= _EPS_BTC:
                continue
            entry = crypto_purchases[purchase_id]
            if entry["Data"] > sale_datetime:
                continue
            eligible.append((entry["Preço BTC"], entry["Data"], purchase_id))
        eligible.sort()

        for buy_price, purchase_datetime, purchase_id in eligible:
            if btc_to_consume <= _EPS_BTC:
                break
            remaining = lots[purchase_id]
            take = min(remaining, btc_to_consume)
            lots[purchase_id] = remaining - take
            if lots[purchase_id] < _EPS_BTC:
                lots[purchase_id] = 0.0
            btc_to_consume -= take

            allocation = {
                "sale_id": sale_id,
                "sale_date": sale_date,
                "sale_datetime": sale_datetime,
                "sale_price": sale_price,
                "purchase_id": purchase_id,
                "purchase_date": purchase_datetime.strftime("%Y-%m-%d"),
                "purchase_datetime": purchase_datetime,
                "buy_price": buy_price,
                "btc_consumed": take,
            }
            allocations.append(allocation)

            if verbose:
                ret = sale_price / buy_price
                print(f"  {sale_id:<10} {purchase_id:<10} "
                      f"{take:>14.8f} {buy_price:>14.2f} "
                      f"{sale_price:>14.2f} {ret:>10.4f}")

        if btc_to_consume > _EPS_BTC:
            raise ValueError(
                f"Sale {sale_id} requires {sale['Reais'] / sale_price:.8f} BTC "
                f"but only {sale['Reais'] / sale_price - btc_to_consume:.8f} BTC "
                f"could be allocated from eligible lots (shortfall "
                f"{btc_to_consume:.8f} BTC)."
            )

    if verbose:
        print()
    return lots, allocations


def build_portfolio(crypto_reference, crypto_purchases, asset, crypto_sales=None):
    """Build a per-purchase portfolio record enriched with sale allocations.

    Args:
        crypto_reference: Reference dataset (date → index/asset values).
        crypto_purchases: Purchases keyed by COMPRA_ ID.
        asset: ``"B3"``, ``"CDI"`` or ``"Bitcoin"``.
        crypto_sales: Optional sales dict keyed by VENDA_ ID.

    Returns:
        Dictionary keyed by purchase_id with rich records::

            {
                'purchase_date':     str (YYYY-MM-DD),
                'purchase_datetime': datetime,
                'reais':             float,
                'asset_value':       float,  # index level or BTC price at buy
                'btc_at_purchase':   float or None,
                'remaining_btc':     float,
                'allocations':       [ {sale_id, sale_date, sale_price,
                                        btc_consumed, buy_price}, ... ],
            }

        Purchases without a usable ``asset_value`` for the requested asset are
        skipped.
    """
    date_to_asset = {
        entry["Data"]: entry.get(asset)
        for entry in crypto_reference.values()
        if asset in entry
    }

    lots, allocations = allocate_sales(crypto_purchases, crypto_sales)

    allocs_by_purchase = {}
    for alloc in allocations:
        allocs_by_purchase.setdefault(alloc["purchase_id"], []).append(alloc)

    portfolio = {}
    for purchase_id, entry in crypto_purchases.items():
        asset_value = entry.get(asset)
        if asset_value is None:
            asset_value = date_to_asset.get(entry["Data"])
        if asset_value is None:
            continue

        portfolio[purchase_id] = {
            "purchase_date":     entry["Data"].strftime("%Y-%m-%d"),
            "purchase_datetime": entry["Data"],
            "reais":             entry["Reais"],
            "asset_value":       asset_value,
            "btc_at_purchase":   entry.get("Bitcoin"),
            "remaining_btc":     lots.get(purchase_id, 0.0),
            "allocations":       allocs_by_purchase.get(purchase_id, []),
        }

    return portfolio


def _slice_brl_in(purchase, btc_amount):
    """BRL invested in a sub-slice of a purchase lot."""
    btc_total = purchase["btc_at_purchase"]
    if btc_total and btc_total > 0:
        return purchase["reais"] * (btc_amount / btc_total)
    # Fallback: pro-rate equally if BTC info is missing (shouldn't happen for crypto_jvm).
    return purchase["reais"]


def _appreciation_rows(portfolio, today_value):
    """Build per-allocation appreciation rows shared by asset & index variants.

    For each purchase, emits one row per sale allocation plus (if any BTC
    remains) one row for the unsold remainder. Preserves the legacy
    ``today_value / brl_invested`` formula for unsold slices.

    Returns ``(rows, weighted)`` where ``rows`` maps a label to an appreciation
    factor and ``weighted`` is the BRL-weighted average across all rows.
    """
    rows = {}
    weighted_sum = 0
    total_investment = 0

    for purchase_id, p in portfolio.items():
        for alloc in p["allocations"]:
            brl_in = _slice_brl_in(p, alloc["btc_consumed"])
            appreciation = alloc["sale_price"] / alloc["buy_price"]
            label = f"{purchase_id}→{alloc['sale_id']}"
            rows[label] = appreciation
            weighted_sum += brl_in * appreciation
            total_investment += brl_in

        remaining = p["remaining_btc"]
        if remaining and remaining > _EPS_BTC and p["btc_at_purchase"]:
            brl_in = _slice_brl_in(p, remaining)
            appreciation = today_value / brl_in
            label = f"{purchase_id} (unsold)"
            rows[label] = appreciation
            weighted_sum += brl_in * appreciation
            total_investment += brl_in

    weighted = weighted_sum / total_investment if total_investment else 0
    return rows, weighted


def calculate_appreciation_asset(portfolio, today_asset_value):
    """Per-allocation Bitcoin appreciation rows + BRL-weighted average."""
    return _appreciation_rows(portfolio, today_asset_value)


def calculate_appreciation_index(portfolio, today_index_value):
    """Per-allocation B3/CDI appreciation rows + BRL-weighted average."""
    return _appreciation_rows(portfolio, today_index_value)


def weighted_unsold_btc_price(crypto_purchases, crypto_sales=None, verbose=False):
    """Weighted-average BTC buy price across remaining (unsold) BTC.

    Weights each purchase lot by its ``remaining_btc`` after the sale-allocation
    pass. Partially-sold lots contribute only their leftover amount.
    """
    lots, _allocs = allocate_sales(crypto_purchases, crypto_sales)
    total_btc = 0
    weighted_sum = 0
    if verbose:
        print("Cálculo do preço médio ponderado (BTC remanescente):")
        header = (f"  {'ID':<12} {'BTC restante':>14} {'Preço BTC':>14} "
                  f"{'BTC × Preço':>14} {'Reais (lote)':>14} {'Status':<28}")
        print(header)
        print("  " + "-" * (len(header) - 2))

    for purchase_id, entry in crypto_purchases.items():
        btc_total = entry.get("Bitcoin")
        price = entry.get("Preço BTC")
        reais = entry.get("Reais")
        remaining = lots.get(purchase_id, 0.0)

        if btc_total is None or price is None:
            status = "descartado (dados ausentes)"
            included = False
        elif remaining <= _EPS_BTC:
            status = "descartado (totalmente vendido)"
            included = False
        elif remaining < btc_total - _EPS_BTC:
            status = "considerado (parcial)"
            included = True
        else:
            status = "considerado"
            included = True

        if verbose:
            btc_str = f"{remaining:.8f}" if btc_total is not None else "—"
            price_str = f"{price:.2f}" if price is not None else "—"
            product_str = (f"{remaining * price:.2f}"
                           if price is not None and btc_total is not None else "—")
            reais_str = f"{reais:.2f}" if reais is not None else "—"
            print(f"  {purchase_id:<12} {btc_str:>14} {price_str:>14} "
                  f"{product_str:>14} {reais_str:>14} {status:<28}")

        if included:
            weighted_sum += remaining * price
            total_btc += remaining

    avg = weighted_sum / total_btc if total_btc else 0
    if verbose:
        print(f"  Σ(BTC × Preço) = {weighted_sum:.6f} BRL")
        print(f"  Σ(BTC)         = {total_btc:.8f} BTC")
        print(f"  Média ponderada = {avg:.2f} BRL/BTC\n")
    return avg


def print_appreciation_table(appreciation_per_label, weighted_average):
    """Prints appreciation data in a tabular format with aligned columns.

    The weighted appreciation is shown only in the last row.

    :param appreciation_per_label: Dictionary {label: appreciation value}
    :param weighted_average: Total weighted appreciation value
    """
    LABEL_WIDTH = 26
    APPRECIATION_WIDTH = 14
    WEIGHTED_WIDTH = 26
    col_widths = {"label": LABEL_WIDTH, "appreciation": APPRECIATION_WIDTH, "weighted": WEIGHTED_WIDTH}

    print(f"{'Alocação':<{col_widths['label']}} "
          f"{'Apreciação':<{col_widths['appreciation']}} "
          f"{'Apreciação Ponderada':<{col_widths['weighted']}}")
    print("-" * (sum(col_widths.values()) + 2))

    items = list(appreciation_per_label.items())
    for idx, (label, appreciation) in enumerate(items):
        weighted_str = f"{weighted_average:.2f}" if idx == len(items) - 1 else ""
        print(f"{label:<{col_widths['label']}} "
              f"{appreciation:<{col_widths['appreciation']}.2f} "
              f"{weighted_str:<{col_widths['weighted']}}")

    print("\n")


def plot_bar_chart(data_dict, ref_list):
    """
    Plots a bar chart using values from a dictionary.

    :param data_dict: Dictionary where keys are labels and values are numerical data.
    :param ref_list: List of reference-line values.
    """
    labels = list(data_dict.keys())
    values = list(data_dict.values())

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color="skyblue", edgecolor="black")

    plt.axhline(ref_list[0], color="red", linestyle="dashed", label=f"Ref 1: {ref_list[0]}")
    cores = ["red", "orange", "green", "blue", "purple"]
    if len(cores) < len(ref_list):
        print("⚠️  Lista de cores insuficiente para o número de referências. Diminua o número de referências ou aumente o número de cores no código-fonte. ⚠️")
    for i, ref in enumerate(ref_list[1:], start=1):
        plt.axhline(ref, color=cores[i], linestyle="dashed", label=f"Ref {i}: {ref}")

    plt.xlabel("Categories")
    plt.ylabel("Values")
    plt.title("Bar Chart with Reference Lines")
    plt.legend()

    plt.xticks(rotation=45)

    plt.show()
