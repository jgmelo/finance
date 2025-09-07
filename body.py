from datetime import datetime
import matplotlib.pyplot as plt

from data import *

crypto_reference = crypto_reference_jvm
crypto_purchases = crypto_jvm

def build_portfolio(crypto_reference, crypto_purchases, asset, crypto_sales=None):
    """Build a portfolio dictionary from purchase and optional sale data.

    Args:
        crypto_reference: Dictionary mapping reference IDs to asset values and dates.
        crypto_purchases: Dictionary mapping purchase IDs to amounts in Reais and purchase dates.
        asset: Key within the reference dictionaries representing the asset value to track
               (e.g. "B3", "CDI", "Bitcoin").
        crypto_sales: Optional dictionary mapping purchase IDs to sale information.

    Returns:
        Dictionary with purchase date (``YYYY-MM-DD``) as key and
        ``[reais_buy, asset_buy_value, sale_date, sale_price]`` as value. ``sale_date`` and
        ``sale_price`` will be ``None`` when no matching sale is found.
    """
    # Create a mapping of dates to asset values
    date_to_asset = {entry["Data"]: entry[asset] for entry in crypto_reference.values()}

    # Build portfolio dictionary
    portfolio = {}
    for purchase_id, entry in crypto_purchases.items():
        date = entry["Data"]
        reais = entry["Reais"]
        asset_value = date_to_asset.get(date, None)  # Get asset points/amount for the same date

        sale_date = None
        sale_price = None
        if crypto_sales is not None:
            sale_entry = crypto_sales.get(purchase_id)
            if sale_entry:
                sale_date = sale_entry["Data"].strftime("%Y-%m-%d")
                sale_price = sale_entry.get("Reais")

        if asset_value is not None:  # Ensure there's a valid asset value
            portfolio[date.strftime("%Y-%m-%d")] = [reais, asset_value, sale_date, sale_price]

    return portfolio

def calculate_appreciation_asset(portfolio, today_asset_value):
    """Calculate asset appreciation.

    Calculates:
      - Asset appreciation per date.
      - Total weighted asset appreciation using investment amounts as weights.
        Sold investments are excluded from the weighted average, and their
        appreciation is based on the ``sale_price`` instead of the current
        ``today_asset_value``.

    Args:
        portfolio: Dictionary where keys are dates (``YYYY-MM-DD``) and values are
            ``[purchase_price, asset_value_at_purchase, sale_date, sale_price]``.
        today_asset_value: Current asset value in Reais.

    Returns:
        Tuple containing:
            - Dictionary with asset appreciation per date.
            - Total weighted asset appreciation (percentage). Returns ``0`` when
              there are no active investments.
    """
    appreciation_per_date = {}
    weighted_sum = 0
    total_investment = 0

    for date, (purchase_price, _asset_value, sale_date, sale_price) in portfolio.items():
        if sale_price is not None:
            appreciation = sale_price / purchase_price
        else:
            appreciation = today_asset_value / purchase_price
            weighted_sum += purchase_price * appreciation
            total_investment += purchase_price

        appreciation_per_date[date] = appreciation

    weighted_appreciation = (
        weighted_sum / total_investment if total_investment else 0
    )

    return appreciation_per_date, weighted_appreciation

def calculate_appreciation_index(portfolio, today_index_value):
    """Calculate index appreciation.

    Calculates:
      - Index appreciation per date.
      - Total weighted index appreciation using investment amounts as weights.
        Sold investments are excluded from the weighted average, and their
        appreciation is based on the ``sale_price`` instead of the current
        ``today_index_value``.

    Args:
        portfolio: Dictionary where keys are dates (``YYYY-MM-DD``) and values are
            ``[purchase_price, index_points_at_purchase, sale_date, sale_price]``.
        today_index_value: Current index quotation in Reais.

    Returns:
        Tuple containing:
            - Dictionary with index appreciation per date.
            - Total weighted index appreciation (percentage). Returns ``0`` when
              there are no active investments.
    """
    appreciation_per_date = {}
    weighted_sum = 0
    total_investment = 0

    for date, (purchase_price, _index_value, sale_date, sale_price) in portfolio.items():
        if sale_price is not None:
            appreciation = sale_price / purchase_price
        else:
            appreciation = today_index_value / purchase_price
            weighted_sum += purchase_price * appreciation
            total_investment += purchase_price

        appreciation_per_date[date] = appreciation

    weighted_appreciation = (
        weighted_sum / total_investment if total_investment else 0
    )

    return appreciation_per_date, weighted_appreciation

def print_appreciation_table(appreciation_per_date, weighted_average):
    """
    Prints appreciation data in a tabular format with aligned columns.
    The weighted appreciation is shown only in the last row.
    
    :param appreciation_per_date: Dictionary {date: appreciation value}
    :param weighted_average: Total weighted appreciation value
    """
    # Define column widths
    DATE_WIDTH = 15
    APPRECIATION_WIDTH = 14
    WEIGHTED_WIDTH = 26
    col_widths = {"date": DATE_WIDTH, "appreciation": APPRECIATION_WIDTH, "weighted": WEIGHTED_WIDTH}

    # Print header
    print(f"{'Data':<{col_widths['date']}} {'Apreciação':<{col_widths['appreciation']}} {'Apreciação Ponderada':<{col_widths['weighted']}}")
    print("-" * (sum(col_widths.values()) + 2))  # Table separator

    # Print each row
    for idx, (date, appreciation) in enumerate(appreciation_per_date.items()):
        weighted_str = f"{weighted_average:.2f}" if idx == len(appreciation_per_date) - 1 else ""  # Show weighted only in last row
        print(f"{date:<{col_widths['date']}} {appreciation:<{col_widths['appreciation']}.2f} {weighted_str:<{col_widths['weighted']}}")
    
    print("\n")


def plot_bar_chart(data_dict, ref_list):
    """
    Plots a bar chart using values from a dictionary.
    
    :param data_dict: Dictionary where keys are labels and values are numerical data.
    :param ref_value1: A float representing the first reference line.
    :param ref_value2: A float representing the second reference line.
    """
    labels = list(data_dict.keys())
    values = list(data_dict.values())

    plt.figure(figsize=(10, 5))  # Set figure size
    plt.bar(labels, values, color="skyblue", edgecolor="black")

    # Add reference lines
    plt.axhline(ref_list[0], color="red", linestyle="dashed", label=f"Ref 1: {ref_list[0]}")
    cores = ["red", "orange", "green", "blue", "purple"]
    if len(cores) < len(ref_list):
        print("⚠️  Lista de cores insuficiente para o número de referências. Diminua o número de referências ou aumente o número de cores no código-fonte. ⚠️")
    for i, ref in enumerate(ref_list[1:], start=1):
        plt.axhline(ref, color=cores[i], linestyle="dashed", label=f"Ref {i}: {ref}")


    # Labels and Title
    plt.xlabel("Categories")
    plt.ylabel("Values")
    plt.title("Bar Chart with Reference Lines")
    plt.legend()
    
    # Rotate x labels for better visibility if needed
    plt.xticks(rotation=45)

    plt.show()