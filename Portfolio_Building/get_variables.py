import json, sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from Corporate_Information.data_ci import *
from Economic_Indicators.data_ei import *

COMPANIES = {0: "NVDA", 1: "KO", 2: "LLY", 3: "JPM", 4: "NFLX"}
COMPANY_COUNT = 5
PROXY = "QUS" # "QQQ" for demo
TREASURY_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'Treasury_Data')
CO_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'Company_Overviews')
ETF_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'ETF_Data')
EXIT_OK = 1
EXIT_FAIL = 0

def _calculate_company_ror(company_ticker: str) -> tuple[float, float]:
    '''
    Calculates the company's required rate of return (ror) from the CAPM.
    Uses the BetaShares S&P 500 Equal Weight ETF as a proxy for the market portfolio.

    Inputs:
    company_ticker: the ticker of the company of interest

    Outputs:
    Tuple of (required rate of return, beta) for the company.
    '''
    # Already extracted relevant information from API
    try:
        file_name = f"{company_ticker}_overview.json"
        file_path = os.path.join(CO_DIRECTORY, file_name)
        with open(file_path, "r") as fp:
            data = json.load(fp)
            beta = float(data["Beta"])
    
    # Create new instance of relevant information from API
    except:
        overview = get_company_overview(company_ticker)
        beta = float(overview["Beta"])

    if not beta:
        print("Failed to retrieve beta.")
        return EXIT_FAIL
    
    try:
        file_name = f"{PROXY}_etf_data.json"
        file_path = os.path.join(ETF_DIRECTORY, file_name)
        with open(file_path) as fp:
            data = json.load(fp)
            rm = float(data["portfolio_turnover"])
    except:
        rm = get_ETF_portfolio_turnover(PROXY)

    if not rm:
        print(f"Failed to retrieve data for {PROXY} (market portfolio proxy)")
        return None
    
    try:
        file_name = f"treasury_data.json"
        file_path = os.path.join(TREASURY_DIRECTORY, file_name)
        with open(file_path) as fp:
            data = json.load(fp)
            rf = float(data["data"][0]["value"]) / 100
    except:
        rf = get_treasury_yield()

    if not rf:
        print(f"Failed to retrieve treasury yield (risk-free rate of return)")
        return None
    
    # Calculate expected ror using CAPM and return
    return (rf + beta * (rm - rf), beta)

def get_variables() -> list[tuple[float, float]]:
    '''
    Gets the variables (rate of return, beta) for the companies listed above.

    Input:
    None

    Output:
    List of (rate of return, beta) pairs for the above companies.
    '''
    ans = []
    for c_number in range(COMPANY_COUNT):
        ans.append(_calculate_company_ror(COMPANIES[c_number]))
    return ans

def get_companies() -> dict[int, str]:
    '''
    Returns the companies selected.

    Input:
    None

    Output:
    A dict mapping the selection order number to the company ticker.
    '''
    return COMPANIES