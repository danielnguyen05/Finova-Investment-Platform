import requests

API_KEY = "T4F7GDVAADDA0L3B"  

def get_company_overview(symbol):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data 
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return None
