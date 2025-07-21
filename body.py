from datetime import datetime
import matplotlib.pyplot as plt

from data import *

crypto_reference = crypto_reference_jvm
crypto_purchases = crypto_jvm

def build_portfolio(crypto_reference, crypto_purchases, asset):
    """
    Builds a portfolio dictionary using investment data from crypto_purchases and IBOVESPA data from crypto_reference.

    :param crypto_reference: Dictionary mapping reference IDs to IBOVESPA points and dates.
    :param crypto_purchases: Dictionary mapping investment IDs to the amount in Reais and investment date.
    :return: Dictionary with date as key and [Reais, B3 points] as value.
    """
    # Create a mapping of dates to asset values
    date_to_asset = {entry["Data"]: entry[asset] for entry in crypto_reference.values()}
    
    # Build portfolio dictionary
    portfolio = {}
    for entry in crypto_purchases.values():
        date = entry["Data"]
        reais = entry["Reais"]
        asset_value = date_to_asset.get(date, None)  # Get asset points for the same date

        if asset_value is not None:  # Ensure there's a valid asset value
            portfolio[date.strftime("%Y-%m-%d")] = [reais, asset_value]

    return portfolio

def calculate_appreciation_asset(portfolio, today_asset_value):
    """
    Calculates:
      - IBOVESPA appreciation per date.
      - Total weighted IBOVESPA appreciation using investment amounts as weights.

    :param portfolio: Dictionary where keys are dates (YYYY-MM-DD),
                      and values are lists [Reais, Asset Amount].
    :param today_asset_value: Asset value points for today.
    :return: Tuple containing:
        - Dictionary with asset appreciation per date.
        - Total weighted asset appreciation (percentage).
    """
    appreciation_per_date = {}
    weighted_sum = 0
    total_investment = 0
    
    for date, (reais, asset_amount) in portfolio.items():
        asset_value = asset_amount / reais
        appreciation = (today_asset_value / (1/asset_value))
        appreciation_per_date[date] = appreciation

        # Compute weighted appreciation
        weighted_sum += reais * appreciation
        total_investment += reais

    weighted_appreciation = weighted_sum / total_investment

    return appreciation_per_date, weighted_appreciation

def calculate_appreciation_index(portfolio, today_index_value):
    """
    Calculates:
      - Index appreciation per date.
      - Total weighted Index appreciation using investment amounts as weights.

    :param portfolio: Dictionary where keys are dates (YYYY-MM-DD),
                      and values are lists [Reais, Index points].
    :param today_index_value: Index quotation for today.
    :return: Tuple containing:
        - Dictionary with Index appreciation per date.
        - Total weighted Index appreciation (percentage).
    """
    appreciation_per_date = {}
    weighted_sum = 0
    total_investment = 0
    
    for date, (reais, index_value) in portfolio.items():
        appreciation = (today_index_value / index_value)
        appreciation_per_date[date] = appreciation

        # Compute weighted appreciation
        weighted_sum += reais * appreciation
        total_investment += reais

    weighted_appreciation = weighted_sum / total_investment

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