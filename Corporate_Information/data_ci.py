import os, json, requests

API_KEY = "demo" # "T4F7GDVAADDA0L3B"  "6Z27NWGRHMUYEX31" "OBUZDCEF32FMATSX" when we do it for real
INDENT = 4
SUCCESS = 200
DIVIDEND_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'Dividend_Data')
CO_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'Company_Overviews')
ETF_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'ETF_Data')

def get_dividends(symbol):
    """
    Fetches dividend data for a given symbol and saves it as a JSON file.
    """
    url = f'https://www.alphavantage.co/query?function=DIVIDENDS&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)

    if response.status_code == SUCCESS:
        data = response.json()

        file_name = f"{symbol}_dividends.json"
        file_path = os.path.join(DIVIDEND_DIRECTORY, file_name)
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=INDENT)
            print(f"Dividend data saved to {file_name}")

        return data
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return None


def get_company_overview(symbol):
    """
    Fetches company overview data for a given symbol and saves it as a JSON file.
    """
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        file_name = f"{symbol}_overview.json"
        file_path = os.path.join(CO_DIRECTORY, file_name)
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=INDENT)
            print(f"Company overview data saved to {file_name}")
        return data
    
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return None

def get_ETF_portfolio_turnover(symbol: str="QQQ") -> float:
    '''
    Extracts ETF data from the API.

    Input:
    symbol: the ticker for the ETF

    Output:
    The portfolio turnover for a specific ETF
    '''
    url = f'https://www.alphavantage.co/query?function=ETF_PROFILE&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)

    if response.status_code == SUCCESS:
        etf_data = response.json()

        file_name = f"{symbol}_etf_data.json"
        file_path = os.path.join(ETF_DIRECTORY, file_name)
        with open(file_path, "w") as json_file:
            json.dump(etf_data, json_file, indent=INDENT)
            print(f"ETF data saved to {file_name}")
        return float(etf_data["portfolio_turnover"])
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return None