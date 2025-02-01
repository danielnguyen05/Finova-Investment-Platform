from Corporate_Information.data_ci import *
from Corporate_Information.graph_ci import *
from Economic_Indicators.data_ei import *
from Economic_Indicators.graph_ei import *
from Portfolio_Building.get_weights import get_weights_given_aggressiveness
from Portfolio_Building.plot_ror import plot_value_given_aggro_and_principal

def main():
    symbol = "IBM"  

    data = get_company_overview(symbol)
    dividends = get_dividends(symbol)

    if data:
        print("\nCompany Overview:")
        print(f"Company Name: {data.get('Name')}")
        print(f"Sector: {data.get('Sector')}")
        print(f"Market Capitalisation: {data.get('MarketCapitalization')}")
        print(f"Description: {data.get('Description')}")
    else:
        print(f"Failed to fetch company overview for {symbol}")

    if dividends and "data" in dividends:
        dividend_data = dividends["data"]
        most_recent = max(dividend_data, key=lambda d: d["ex_dividend_date"])
        highest_paying = max(dividend_data, key=lambda d: float(d["amount"]))

        print("\nDividend Information:")
        print("Most Recent Dividend:")
        print(f"  - Ex-Dividend Date: {most_recent['ex_dividend_date']}")
        print(f"  - Declaration Date: {most_recent['declaration_date']}")
        print(f"  - Record Date: {most_recent['record_date']}")
        print(f"  - Payment Date: {most_recent['payment_date']}")
        print(f"  - Amount: {most_recent['amount']}")

        print("\nHighest-Paying Dividend:")
        print(f"  - Ex-Dividend Date: {highest_paying['ex_dividend_date']}")
        print(f"  - Declaration Date: {highest_paying['declaration_date']}")
        print(f"  - Record Date: {highest_paying['record_date']}")
        print(f"  - Payment Date: {highest_paying['payment_date']}")
        print(f"  - Amount: {highest_paying['amount']}")
    else:
        print(f"Failed to fetch dividend data for {symbol}")
    
    # # Example execution
    # sample_test_data = get_real_gdp()

    # if sample_test_data:
    #     plot_real_gdp(sample_test_data)
    
    # Sample execution
    # plot_dividends_overlay(symbol)
    
    # Sample Execution:
    print(get_weights_given_aggressiveness("conservative")) # conservative, moderately conservative, moderately aggressive, aggressive
    plot_value_given_aggro_and_principal("conservative", 500) # saved as a .png file

if __name__ == "__main__":
    main()