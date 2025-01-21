from Corporate_Information.data_ci import get_company_overview
from Economic_Indicators.data_ei import *
from Economic_Indicators.graph_ei import *

def main():
    symbol = "AAPL"  
    data = get_company_overview(symbol)

    if data:
        print(f"Company Name: {data.get('Name')}")
        print(f"Sector: {data.get('Sector')}")
        print(f"Market Capitalisation: {data.get('MarketCapitalization')}")
        print(f"Description: {data.get('Description')}")

if __name__ == "__main__":
    main()
