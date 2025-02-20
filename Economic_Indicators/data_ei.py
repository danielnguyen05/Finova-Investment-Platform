import requests, json, os

API_KEY_2 = "6Z27NWGRHMUYEX31" # "T4F7GDVAADDA0L3B"  "6Z27NWGRHMUYEX31" "OBUZDCEF32FMATSX" when we do it for real
SUCCESS = 200
INDENT = 4
GDP_FNAME = "Real_GDP.json"
TREASURY_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'Treasury_Data')

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

def get_real_gdp_per_capita() -> dict:
    '''
    Fetches the Real GDP per Capita from the API.

    Input:
    None

    Output:
    dict containing all relevant information.
    '''
    url = f'https://www.alphavantage.co/query?function=REAL_GDP_PER_CAPITA&apikey={API_KEY_2}'
    response = requests.get(url)

    if response.status_code == SUCCESS:
        return response.json()  
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return None

def get_treasury_yield() -> float:
    '''
    Gets the yield to maturity (YTM), assuming monthly interval and 10-year maturity.

    Input:
    None

    Output:
    YTM, as a decimal.
    '''
    url = f"https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey={API_KEY_2}"
    response = requests.get(url)

    if response.status_code == SUCCESS:
        treasury_data = response.json()
        fname = "treasury_data.json"
        file_path = os.path.join(TREASURY_DIRECTORY, fname)
        with open(file_path, "w") as json_file:
            json.dump(treasury_data, json_file, indent=INDENT)  
            print(f"Treasury yield information saved to {fname}")
        return float(treasury_data["data"][0]["value"]) / 100
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return None