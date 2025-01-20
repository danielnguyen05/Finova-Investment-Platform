import requests
import json

API_KEY = "T4F7GDVAADDA0L3B"  

def get_company_overview(symbol):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()

        file_name = f"{symbol}_overview.json"
        with open(file_name, "w") as json_file:
            json.dump(data, json_file, indent=4)  
            print(f"JSON data saved to {file_name}")

        return data 
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return None
