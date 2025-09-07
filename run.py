BRL_POR_BTC_REF    = 669550.50
BTC_POR_BRL_REF    = 1/BRL_POR_BTC_REF
CDI_REF            = 0.95
B3_REF             = 135298.98

from body import *
from data import crypto_sales

portfolio = build_portfolio(crypto_reference=crypto_reference,
                            crypto_purchases=crypto_purchases,
                            asset="B3",
                            crypto_sales=crypto_sales)
appreciation_per_date_b3, weighted_b3 = calculate_appreciation_index(
    portfolio=portfolio, today_index_value=B3_REF)
print("B3:")
print_appreciation_table(appreciation_per_date_b3, weighted_b3)

portfolio_cdi = build_portfolio(crypto_reference=crypto_reference,
                                crypto_purchases=crypto_purchases,
                                asset="CDI",
                                crypto_sales=crypto_sales)
appreciation_per_date_cdi, weighted_cdi = calculate_appreciation_index(
    portfolio=portfolio_cdi, today_index_value=CDI_REF)
print("CDI:")
print_appreciation_table(appreciation_per_date_cdi, weighted_cdi)

# Include realized sale information for the crypto portfolio
portfolio_bitcoin = build_portfolio(crypto_reference=crypto_reference,
                                    crypto_purchases=crypto_purchases,
                                    asset="Bitcoin",
                                    crypto_sales=crypto_sales)
appreciation_per_date_btc, weighted_btc = calculate_appreciation_asset(
    portfolio=portfolio_bitcoin, today_asset_value=BRL_POR_BTC_REF)
print("Bitcoin:")
print_appreciation_table(appreciation_per_date_btc, weighted_btc)

print("Sample sale entries:")
for pid, sale in list(crypto_sales.items())[:2]:
    print(f"{pid} sold on {sale['Data'].strftime('%Y-%m-%d')} for {sale['Reais']:.2f} BRL")

plot_bar_chart(appreciation_per_date_btc,
               [weighted_btc, weighted_b3, 1.5*(weighted_b3-1)+1, 2*(weighted_b3-1)+1])
