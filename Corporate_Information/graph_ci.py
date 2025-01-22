import matplotlib.pyplot as plt
from datetime import datetime

def plot_dividend_trends(dividends_data, symbol):
    """
    Plots dividend trends for a given company based on dividend data.
    """
    if not dividends_data or "data" not in dividends_data:
        print("Invalid or missing dividend data.")
        return
    
    dividend_records = dividends_data["data"]

    dates = [datetime.strptime(record['ex_dividend_date'], '%Y-%m-%d') for record in dividend_records]
    amounts = [float(record['amount']) for record in dividend_records]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, amounts, marker='o', linestyle='-', label='Dividend Amount')
    plt.title(f"Dividend Trends for {symbol}")
    plt.xlabel("Ex-Dividend Date")
    plt.ylabel("Dividend Amount ($)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
