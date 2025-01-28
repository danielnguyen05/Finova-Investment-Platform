import pulp, json
from Corporate_Information.data_ci import *
from Economic_Indicators.data_ei import *

COMPANY_1 = "AAPL" # Apple: tech
COMPANY_2 = "KO" # Coca-cola: food
COMPANY_3 = "PFE" # Pfizer: medicine
COMPANY_4 = "BAC" # Bank of America: bank
COMPANY_5 = "MTU" # Mitsubishi: cars
PROXY = "QUS"

def calculate_company_ror(company_ticker: str) -> tuple[float, float]:
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
        with open(f"{company_ticker}_overview.json", "r") as fp:
            data = json.load(fp)
            beta = data["Beta"]
    
    # Create new instance of relevant information from API
    except:
        overview = get_company_overview(company_ticker)
        beta = overview["Beta"]

    if not beta:
        print("Failed to retrieve beta")
        return None
    
    rm = get_ETF_portfolio_turnover(PROXY)

    if not rm:
        print(f"Failed to retrieve data for {PROXY} (market portfolio proxy)")
        return None
    
    rf = get_treasury_yield()

    if not rf:
        print(f"Failed to retrieve treasury yield (risk-free rate of return)")
        return None
    
    return tuple(rf + beta * (rm - rf), beta)

print(calculate_company_ror("IBM"))