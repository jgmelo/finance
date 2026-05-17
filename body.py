from datetime import datetime
import matplotlib.pyplot as plt

from data import *

crypto_reference = crypto_reference_jvm
crypto_purchases = crypto_jvm

_EPS_QTY = 1e-12

# Cryptos appear in `crypto_jvm` entries via the 'Cripto' field; indexes are
# named explicitly by build_portfolio's `asset` argument.
INDEX_ASSETS = {"B3", "CDI"}


def allocate_sales(crypto_purchases, crypto_sales=None, verbose=False):
    """Match sales against purchase lots, cheapest-cost-basis-first, per crypto.

    Sales and purchases are grouped by their ``Cripto`` field; allocation
    happens independently per crypto. For each sale (in chronological order),
    the quantity ``Reais / Preço`` is consumed from eligible lots of the same
    crypto whose ``Data`` is on or before the sale date, sorted by ascending
    ``Preço`` (ties broken by oldest purchase date).

    Raises:
        ValueError: when the total quantity requested by sales of any crypto
            exceeds what is available from eligible lots of that crypto.

    Returns:
        Tuple ``(lots, allocations)`` where:
            - ``lots`` is ``{purchase_id: remaining_qty}``.
            - ``allocations`` is a list of dicts, in execution order:
              ``{sale_id, sale_date, sale_datetime, sale_price, cripto,
                 purchase_id, purchase_date, purchase_datetime,
                 buy_price, qty_consumed}``.
    """
    sales = crypto_sales or {}

    lots = {}
    for purchase_id, entry in crypto_purchases.items():
        qty = entry.get("Quantidade")
        if qty is None:
            continue
        lots[purchase_id] = qty

    allocations = []
    if verbose:
        print("Alocação de vendas (mais barato primeiro):")
        header = (f"  {'Cripto':<10} {'Venda':<10} {'Compra':<10} "
                  f"{'Qtd consumida':>14} {'Preço compra':>14} "
                  f"{'Preço venda':>14} {'Retorno':>10}")
        print(header)
        print("  " + "-" * (len(header) - 2))

    sorted_sales = sorted(sales.items(), key=lambda kv: kv[1]["Data"])
    for sale_id, sale in sorted_sales:
        cripto = sale["Cripto"]
        sale_price = sale["Preço"]
        qty_to_consume = sale["Reais"] / sale_price
        qty_requested = qty_to_consume
        sale_datetime = sale["Data"]
        sale_date = sale_datetime.strftime("%Y-%m-%d")

        eligible = []
        for purchase_id, remaining in lots.items():
            if remaining <= _EPS_QTY:
                continue
            entry = crypto_purchases[purchase_id]
            if entry.get("Cripto") != cripto:
                continue
            if entry["Data"] > sale_datetime:
                continue
            eligible.append((entry["Preço"], entry["Data"], purchase_id))
        eligible.sort()

        for buy_price, purchase_datetime, purchase_id in eligible:
            if qty_to_consume <= _EPS_QTY:
                break
            remaining = lots[purchase_id]
            take = min(remaining, qty_to_consume)
            lots[purchase_id] = remaining - take
            if lots[purchase_id] < _EPS_QTY:
                lots[purchase_id] = 0.0
            qty_to_consume -= take

            allocation = {
                "sale_id": sale_id,
                "sale_date": sale_date,
                "sale_datetime": sale_datetime,
                "sale_price": sale_price,
                "cripto": cripto,
                "purchase_id": purchase_id,
                "purchase_date": purchase_datetime.strftime("%Y-%m-%d"),
                "purchase_datetime": purchase_datetime,
                "buy_price": buy_price,
                "qty_consumed": take,
            }
            allocations.append(allocation)

            if verbose:
                ret = sale_price / buy_price
                print(f"  {cripto:<10} {sale_id:<10} {purchase_id:<10} "
                      f"{take:>14.8f} {buy_price:>14.2f} "
                      f"{sale_price:>14.2f} {ret:>10.4f}")

        if qty_to_consume > _EPS_QTY:
            raise ValueError(
                f"Sale {sale_id} ({cripto}) requires {qty_requested:.8f} units "
                f"but only {qty_requested - qty_to_consume:.8f} could be "
                f"allocated from eligible lots (shortfall {qty_to_consume:.8f})."
            )

    if verbose:
        print()
    return lots, allocations


def build_portfolio(crypto_reference, crypto_purchases, asset, crypto_sales=None):
    """Build a per-purchase portfolio record enriched with sale allocations.

    Args:
        crypto_reference: Reference dataset (date → index/asset values).
        crypto_purchases: Purchases keyed by COMPRA_ ID.
        asset: Either a crypto symbol present in any purchase's ``Cripto``
            field (e.g. ``"Bitcoin"``, ``"Ethereum"``) or an index name in
            ``INDEX_ASSETS`` (``"B3"``, ``"CDI"``).
        crypto_sales: Optional sales dict keyed by VENDA_ ID.

    Returns:
        Dictionary keyed by purchase_id with rich records::

            {
                'purchase_date':         str (YYYY-MM-DD),
                'purchase_datetime':     datetime,
                'reais':                 float,
                'cripto':                str,
                'asset_value':           float,  # index level or Preço at buy
                'quantidade_at_purchase': float or None,
                'remaining_qty':         float,
                'allocations':           [ {sale_id, sale_date, sale_price,
                                            qty_consumed, buy_price, cripto}, ... ],
            }

        When ``asset`` is a crypto symbol, only purchases of that crypto are
        included. When ``asset`` is an index name, all purchases that match a
        reference-date entry are included.
    """
    lots, allocations = allocate_sales(crypto_purchases, crypto_sales)

    allocs_by_purchase = {}
    for alloc in allocations:
        allocs_by_purchase.setdefault(alloc["purchase_id"], []).append(alloc)

    is_index = asset in INDEX_ASSETS
    date_to_asset = (
        {entry["Data"]: entry.get(asset)
         for entry in crypto_reference.values() if asset in entry}
        if is_index else {}
    )

    portfolio = {}
    for purchase_id, entry in crypto_purchases.items():
        if is_index:
            asset_value = date_to_asset.get(entry["Data"])
        else:
            if entry.get("Cripto") != asset:
                continue
            asset_value = entry.get("Preço")

        if asset_value is None:
            continue

        portfolio[purchase_id] = {
            "purchase_date":          entry["Data"].strftime("%Y-%m-%d"),
            "purchase_datetime":      entry["Data"],
            "reais":                  entry["Reais"],
            "cripto":                 entry.get("Cripto"),
            "asset_value":            asset_value,
            "quantidade_at_purchase": entry.get("Quantidade"),
            "remaining_qty":          lots.get(purchase_id, 0.0),
            "allocations":            allocs_by_purchase.get(purchase_id, []),
        }

    return portfolio


def _slice_brl_in(purchase, qty_amount):
    """BRL invested in a sub-slice of a purchase lot."""
    qty_total = purchase["quantidade_at_purchase"]
    if qty_total and qty_total > 0:
        return purchase["reais"] * (qty_amount / qty_total)
    return purchase["reais"]


def _appreciation_rows(portfolio, today_value):
    """Build per-allocation appreciation rows shared by asset & index variants.

    For each purchase, emits one row per sale allocation plus (if any quantity
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
            brl_in = _slice_brl_in(p, alloc["qty_consumed"])
            appreciation = alloc["sale_price"] / alloc["buy_price"]
            label = f"{purchase_id}→{alloc['sale_id']}"
            rows[label] = appreciation
            weighted_sum += brl_in * appreciation
            total_investment += brl_in

        remaining = p["remaining_qty"]
        if remaining and remaining > _EPS_QTY and p["quantidade_at_purchase"]:
            brl_in = _slice_brl_in(p, remaining)
            appreciation = today_value / brl_in
            label = f"{purchase_id} (unsold)"
            rows[label] = appreciation
            weighted_sum += brl_in * appreciation
            total_investment += brl_in

    weighted = weighted_sum / total_investment if total_investment else 0
    return rows, weighted


def calculate_appreciation_asset(portfolio, today_asset_value):
    """Per-allocation crypto appreciation rows + BRL-weighted average."""
    return _appreciation_rows(portfolio, today_asset_value)


def calculate_appreciation_index(portfolio, today_index_value):
    """Per-allocation B3/CDI appreciation rows + BRL-weighted average."""
    return _appreciation_rows(portfolio, today_index_value)


def weighted_unsold_price(crypto_purchases, crypto_sales=None, cripto="Bitcoin",
                          verbose=False):
    """Weighted-average buy price across remaining (unsold) units of ``cripto``.

    Weights each purchase lot by its ``remaining_qty`` after the sale-allocation
    pass. Partially-sold lots contribute only their leftover amount. Returns
    ``0`` when no remaining units exist for that crypto.
    """
    lots, _allocs = allocate_sales(crypto_purchases, crypto_sales)
    total_qty = 0
    weighted_sum = 0
    if verbose:
        print(f"Cálculo do preço médio ponderado ({cripto} remanescente):")
        header = (f"  {'ID':<12} {'Qtd restante':>14} {'Preço':>14} "
                  f"{'Qtd × Preço':>14} {'Reais (lote)':>14} {'Status':<32}")
        print(header)
        print("  " + "-" * (len(header) - 2))

    for purchase_id, entry in crypto_purchases.items():
        if entry.get("Cripto") != cripto:
            continue
        qty_total = entry.get("Quantidade")
        price = entry.get("Preço")
        reais = entry.get("Reais")
        remaining = lots.get(purchase_id, 0.0)

        if qty_total is None or price is None:
            status = "descartado (dados ausentes)"
            included = False
        elif remaining <= _EPS_QTY:
            status = "descartado (totalmente vendido)"
            included = False
        elif remaining < qty_total - _EPS_QTY:
            status = "considerado (parcial)"
            included = True
        else:
            status = "considerado"
            included = True

        if verbose:
            qty_str = f"{remaining:.8f}" if qty_total is not None else "—"
            price_str = f"{price:.2f}" if price is not None else "—"
            product_str = (f"{remaining * price:.2f}"
                           if price is not None and qty_total is not None else "—")
            reais_str = f"{reais:.2f}" if reais is not None else "—"
            print(f"  {purchase_id:<12} {qty_str:>14} {price_str:>14} "
                  f"{product_str:>14} {reais_str:>14} {status:<32}")

        if included:
            weighted_sum += remaining * price
            total_qty += remaining

    avg = weighted_sum / total_qty if total_qty else 0
    if verbose:
        print(f"  Σ(Qtd × Preço) = {weighted_sum:.6f} BRL")
        print(f"  Σ(Qtd)         = {total_qty:.8f} {cripto}")
        print(f"  Média ponderada = {avg:.2f} BRL/{cripto}\n")
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


def plot_bar_chart(data_dict, ref_list, title="Bar Chart with Reference Lines"):
    """
    Plots a bar chart using values from a dictionary.

    :param data_dict: Dictionary where keys are labels and values are numerical data.
    :param ref_list: List of reference-line values.
    :param title: Chart title.
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
    plt.title(title)
    plt.legend()

    plt.xticks(rotation=45)

    plt.show()
