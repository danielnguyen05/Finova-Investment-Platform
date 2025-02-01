import matplotlib.pyplot as plt
from datetime import datetime
import sys, os, json

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from Corporate_Information.data_ci import get_dividends

EXIT_OK = 1
EXIT_FAIL = 0

def plot_dividends_overlay(companies: list[str]):
    '''
    Plots the dividend trends of one more more companies on top of each other.

    Input:
    companies: a list of tickers for the companies.

    Output:
    A plot of the dividend data of the companies required, with plots overlaid.
    '''
    num_companies = len(companies)

    if num_companies == 0:
        print("Error - not enough companies selected.")
        return EXIT_FAIL
    
    plt.figure(figsize=(10, 6))

    for company_number in range(num_companies):
        try:
            fname = f"{companies[company_number]}_dividends.json"
            with open(fname, 'r') as fp:
                dividend_data = json.load(fp)
        except:
            dividend_data = get_dividends(companies[company_number])

        if "data" not in dividend_data:
            print("Invalid or missing dividend data.")
            plt.close()
            return EXIT_FAIL
        
        dividend_data = dividend_data["data"]

        dates = [datetime.strptime(record['ex_dividend_date'], '%Y-%m-%d') for record in dividend_data]
        amounts = [float(record['amount']) for record in dividend_data]
        plt.plot(dates, amounts, linestyle='-', label=companies[company_number])

    plt.title(f"Dividend Trends for {', '.join(companies)}")
    plt.xlabel("Ex-Dividend Date")
    plt.ylabel("Dividend Amount ($)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("company_dividends_plot.png")
    plt.close()
    return EXIT_OK