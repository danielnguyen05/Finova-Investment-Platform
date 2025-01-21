import requests, json

API_KEY_2 = "DEMO" # 6Z27NWGRHMUYEX31 for when we wanna do it fr
SUCCESS = 200
GDP_FNAME = "Real_GDP.json"

def get_real_gdp(interval: str) -> dict:
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
            json.dump(gdp_data, json_file, indent=4)  
            print(f"JSON data saved to {GDP_FNAME}")

        return gdp_data 
    
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return None

