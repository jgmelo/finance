import argparse

from body import *
from data import crypto_sales

DEFAULT_BRL_POR_BTC_REF = 669550.50
DEFAULT_CDI_REF         = 0.95
DEFAULT_B3_REF          = 135298.98

ASSET_CHOICES = ["b3", "cdi", "bitcoin", "all"]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compute and display portfolio appreciation across assets.")
    parser.add_argument("--asset", choices=ASSET_CHOICES, action="append",
                        help="Asset section to include. Repeatable. "
                             "Defaults to 'all' when omitted.")
    parser.add_argument("--brl-per-btc", type=float, default=DEFAULT_BRL_POR_BTC_REF,
                        help="Current BRL per BTC reference price.")
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
                        help="Show the per-entry breakdown of the unsold-BTC "
                             "weighted-average price calculation.")
    parser.add_argument("--verbose-alloc", action="store_true",
                        help="Show the sale → purchase-lot allocation table "
                             "(cheapest-cost-basis-first).")
    return parser.parse_args()


def selected_assets(asset_args):
    if not asset_args or "all" in asset_args:
        return ["b3", "cdi", "bitcoin"]
    return list(dict.fromkeys(asset_args))


def main():
    args = parse_args()
    assets = selected_assets(args.asset)

    if args.verbose_alloc:
        allocate_sales(crypto_purchases, crypto_sales, verbose=True)

    weighted_b3 = None
    appreciation_per_date_btc = None
    weighted_btc = None

    if "b3" in assets:
        portfolio = build_portfolio(crypto_reference=crypto_reference,
                                    crypto_purchases=crypto_purchases,
                                    asset="B3",
                                    crypto_sales=crypto_sales)
        appreciation_per_date_b3, weighted_b3 = calculate_appreciation_index(
            portfolio=portfolio, today_index_value=args.b3_ref)
        print("B3:")
        print_appreciation_table(appreciation_per_date_b3, weighted_b3)

    if "cdi" in assets:
        portfolio_cdi = build_portfolio(crypto_reference=crypto_reference,
                                        crypto_purchases=crypto_purchases,
                                        asset="CDI",
                                        crypto_sales=crypto_sales)
        appreciation_per_date_cdi, weighted_cdi = calculate_appreciation_index(
            portfolio=portfolio_cdi, today_index_value=args.cdi_ref)
        print("CDI:")
        print_appreciation_table(appreciation_per_date_cdi, weighted_cdi)

    if "bitcoin" in assets:
        portfolio_bitcoin = build_portfolio(crypto_reference=crypto_reference,
                                            crypto_purchases=crypto_purchases,
                                            asset="Bitcoin",
                                            crypto_sales=crypto_sales)
        appreciation_per_date_btc, weighted_btc = calculate_appreciation_asset(
            portfolio=portfolio_bitcoin, today_asset_value=args.brl_per_btc)
        print("Bitcoin:")
        print_appreciation_table(appreciation_per_date_btc, weighted_btc)

        avg_unsold_price = weighted_unsold_btc_price(
            crypto_purchases, crypto_sales, verbose=args.verbose_avg)
        print(f"Preço médio ponderado (posições não vendidas): "
              f"{avg_unsold_price:.2f} BRL/BTC\n")

    if args.show_sales:
        print("Sample sale entries:")
        for pid, sale in list(crypto_sales.items())[:args.sales_limit]:
            print(f"{pid} sold on {sale['Data'].strftime('%Y-%m-%d')} "
                  f"for {sale['Reais']:.2f} BRL")

    if args.plot:
        if appreciation_per_date_btc is None or weighted_btc is None or weighted_b3 is None:
            print("Skipping plot: requires both 'bitcoin' and 'b3' assets to be selected.")
        else:
            plot_bar_chart(appreciation_per_date_btc,
                           [weighted_btc, weighted_b3,
                            1.5 * (weighted_b3 - 1) + 1,
                            2 * (weighted_b3 - 1) + 1])


if __name__ == "__main__":
    main()
