import argparse

from body import *
from data import crypto_sales

DEFAULT_REFS = {
    "Bitcoin":  669550.50,
    "Ethereum": 22000.0,
}
DEFAULT_CDI_REF = 0.95
DEFAULT_B3_REF  = 135298.98

CRYPTO_ASSETS = ["bitcoin", "ethereum"]
INDEX_ASSETS  = ["b3", "cdi"]
ASSET_CHOICES = INDEX_ASSETS + CRYPTO_ASSETS + ["all"]

CRYPTO_DISPLAY = {"bitcoin": "Bitcoin", "ethereum": "Ethereum"}


def _parse_ref(value):
    if "=" not in value:
        raise argparse.ArgumentTypeError(
            f"--ref expects Cripto=Value (got {value!r})")
    name, raw = value.split("=", 1)
    try:
        return name.strip(), float(raw)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"--ref value for {name!r} is not a number: {raw!r}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compute and display portfolio appreciation across assets.")
    parser.add_argument("--asset", choices=ASSET_CHOICES, action="append",
                        help="Asset section to include. Repeatable. "
                             "Defaults to 'all' when omitted.")
    parser.add_argument("--ref", type=_parse_ref, action="append", default=[],
                        metavar="Cripto=Value",
                        help="Override the 'today' BRL price for a crypto, "
                             "e.g. --ref Bitcoin=669550.50. Repeatable.")
    parser.add_argument("--cdi-ref", type=float, default=DEFAULT_CDI_REF,
                        help="Current CDI reference index value.")
    parser.add_argument("--b3-ref", type=float, default=DEFAULT_B3_REF,
                        help="Current B3 reference index value.")
    parser.add_argument("--plot", dest="plot", action="store_true",
                        help="Show the bar chart (default).")
    parser.add_argument("--no-plot", dest="plot", action="store_false",
                        help="Skip the bar chart.")
    parser.set_defaults(plot=True)
    parser.add_argument("--show-sales", dest="show_sales", action="store_true",
                        help="Print sample sale entries (default).")
    parser.add_argument("--no-show-sales", dest="show_sales", action="store_false",
                        help="Skip sample sale entries.")
    parser.set_defaults(show_sales=True)
    parser.add_argument("--sales-limit", type=int, default=2,
                        help="How many sample sale entries to print.")
    parser.add_argument("--verbose-avg", action="store_true",
                        help="Show the per-entry breakdown of the unsold-crypto "
                             "weighted-average price calculation.")
    parser.add_argument("--verbose-alloc", action="store_true",
                        help="Show the sale → purchase-lot allocation table "
                             "(cheapest-cost-basis-first).")
    return parser.parse_args()


def selected_assets(asset_args):
    if not asset_args or "all" in asset_args:
        return INDEX_ASSETS + CRYPTO_ASSETS
    return list(dict.fromkeys(asset_args))


def resolve_refs(ref_args):
    refs = dict(DEFAULT_REFS)
    for name, value in ref_args:
        refs[name] = value
    return refs


def main():
    args = parse_args()
    assets = selected_assets(args.asset)
    refs = resolve_refs(args.ref)

    if args.verbose_alloc:
        allocate_sales(crypto_purchases, crypto_sales, verbose=True)

    weighted_b3 = None
    crypto_results = {}  # cripto_display → (rows, weighted)

    if "b3" in assets:
        portfolio = build_portfolio(crypto_reference=crypto_reference,
                                    crypto_purchases=crypto_purchases,
                                    asset="B3",
                                    crypto_sales=crypto_sales)
        rows_b3, weighted_b3 = calculate_appreciation_index(
            portfolio=portfolio, today_index_value=args.b3_ref)
        print("B3:")
        print_appreciation_table(rows_b3, weighted_b3)

    if "cdi" in assets:
        portfolio_cdi = build_portfolio(crypto_reference=crypto_reference,
                                        crypto_purchases=crypto_purchases,
                                        asset="CDI",
                                        crypto_sales=crypto_sales)
        rows_cdi, weighted_cdi = calculate_appreciation_index(
            portfolio=portfolio_cdi, today_index_value=args.cdi_ref)
        print("CDI:")
        print_appreciation_table(rows_cdi, weighted_cdi)

    for crypto_key in CRYPTO_ASSETS:
        if crypto_key not in assets:
            continue
        cripto = CRYPTO_DISPLAY[crypto_key]
        today_value = refs.get(cripto)
        if today_value is None:
            print(f"Skipping {cripto}: no reference price (use --ref {cripto}=…).\n")
            continue

        portfolio = build_portfolio(crypto_reference=crypto_reference,
                                    crypto_purchases=crypto_purchases,
                                    asset=cripto,
                                    crypto_sales=crypto_sales)
        if not portfolio:
            print(f"Skipping {cripto}: no purchase lots found.\n")
            continue

        rows, weighted = calculate_appreciation_asset(
            portfolio=portfolio, today_asset_value=today_value)
        print(f"{cripto}:")
        print_appreciation_table(rows, weighted)

        avg_unsold = weighted_unsold_price(
            crypto_purchases, crypto_sales, cripto=cripto,
            verbose=args.verbose_avg)
        print(f"Preço médio ponderado (posições não vendidas) {cripto}: "
              f"{avg_unsold:.2f} BRL/{cripto}\n")

        crypto_results[cripto] = (rows, weighted)

    if args.show_sales:
        print("Sample sale entries:")
        for sid, sale in list(crypto_sales.items())[:args.sales_limit]:
            print(f"{sid} ({sale['Cripto']}) on {sale['Data'].strftime('%Y-%m-%d')} "
                  f"for {sale['Reais']:.2f} BRL")
        print()

    if args.plot:
        if weighted_b3 is None:
            print("Skipping plot: requires the 'b3' asset for reference lines.")
        elif not crypto_results:
            print("Skipping plot: no crypto sections were computed.")
        else:
            for cripto, (rows, weighted) in crypto_results.items():
                plot_bar_chart(
                    rows,
                    [weighted, weighted_b3,
                     1.5 * (weighted_b3 - 1) + 1,
                     2 * (weighted_b3 - 1) + 1],
                    title=f"{cripto} appreciation vs. references")


if __name__ == "__main__":
    main()
