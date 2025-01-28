import requests, json

API_KEY_2 = "demo" # 6Z27NWGRHMUYEX31 for when we wanna do it fr
SUCCESS = 200
INDENT = 4
GDP_FNAME = "Real_GDP.json"

def get_real_gdp(interval: str="annual") -> dict:
    '''
    Grabs the real GDP from the API.

    Input:
    Interval: quarterly/annual.

    Output:
    dict containing all relevant information.
    '''
    url = f'https://www.alphavantage.co/query?function=REAL_GDP&interval={interval}&apikey={API_KEY_2}'
    response = requests.get(url)

    if response.status_code == SUCCESS:
        gdp_data = response.json()

        with open(GDP_FNAME, "w") as json_file:
            json.dump(gdp_data, json_file, indent=INDENT)  
            print(f"JSON data saved to {GDP_FNAME}")

        return gdp_data 
    
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return None

#TODO:  Oi remember to the Real_GDP_Per_Capita one ye

def get_ETF_data(symbol: str="QQQ") -> dict:
    '''
    Extracts ETF data from the API.

    Input:
    symbol: the ticker for the ETF

    Output:
    dict containing all relevant information.
    '''
    url = f'https://www.alphavantage.co/query?function=ETF_PROFILE&symbol={symbol}&apikey={API_KEY_2}'
    response = requests.get(url)

    if response.status_code == SUCCESS:
        etf_data = response.json()

        with open(f"{symbol}_Information", "w") as json_file:
            json.dump(etf_data, json_file, indent=INDENT)  
            print(f"JSON data saved to {symbol}_Information")

        return etf_data