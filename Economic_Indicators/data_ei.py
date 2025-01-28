import requests

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
        return gdp_data 
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return None

#TODO:  Oi remember to the Real_GDP_Per_Capita one ye

def get_treasury_yield() -> float:
    '''
    Gets the yield to maturity (YTM), assuming monthly interval and 30-year maturity.

    Input:
    None

    Output:
    YTM, as a decimal.
    '''
    url = "https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=30year&apikey={API_KEY_2}"
    response = requests.get(url)

    if response.status_code == SUCCESS:
        treasury_data = response.json()
        return float(treasury_data["data"][0]["value"]) / 100
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return None