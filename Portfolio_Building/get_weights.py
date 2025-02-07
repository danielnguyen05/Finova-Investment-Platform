import sys, os, pandas, json
from pulp import LpProblem, LpVariable, lpSum, LpMaximize, value, PULP_CBC_CMD
from random import randint
import numpy as np

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from Portfolio_Building.get_variables import get_variables, get_companies
from Corporate_Information.data_ci import get_covariance_matrix

COV_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'Covariance_Matrices_Data')
COMPANY_COUNT = 5
Z_SCORE = 1

def _get_weights(threshold: float, expected_ror: list[float], beta: list[float]) -> tuple[list[float], float]:
    '''
    Gets the optimal weights for each company to maximize expected return while meeting a beta constraint.

    Input:
    - threshold: The required beta for the portfolio.
    - expected_ror: List of expected rates of returns for companies.
    - beta: List of beta values for the companies.

    Output:
    - Tuple (list of weights, maximum expected return)
    '''
    problem = LpProblem("Maximise_Expected_RoR_Given_Beta", LpMaximize)
    weights = [LpVariable(f"w_{i+1}", lowBound=randint(1, 5)/100, upBound=randint(37, 43)/100) for i in range(COMPANY_COUNT)]
    problem += lpSum(weights) == 1
    problem += lpSum(weights[i] * beta[i] for i in range(COMPANY_COUNT)) <= threshold
    problem += lpSum(weights[i] * expected_ror[i] for i in range(COMPANY_COUNT))
    problem.solve(PULP_CBC_CMD(msg=False))  
    weights = [value(w) for w in weights]
    return weights, value(problem.objective)

def get_weights_given_aggressiveness(aggressiveness: str) -> tuple[list[float], float]:
    '''
    Returns optimal portfolio weights based on the chosen level of risk aggressiveness.

    Input:
    - aggressiveness: "conservative", "moderately conservative", "moderately aggressive", "aggressive".

    Output:
    - Tuple (list of weights, target expected rate of return).
    '''
    to_be_processed = get_variables()
    expected_ror, beta = [elem[0] for elem in to_be_processed], [elem[1] for elem in to_be_processed]
    sorted_beta = sorted(beta)

    if aggressiveness == "conservative":
        target_beta = (sorted_beta[0] + sorted_beta[1]) / 2 + 0.15 # Stops LP from cycling
    elif aggressiveness == "moderately conservative":
        target_beta = (sorted_beta[1] + sorted_beta[2]) / 2
    elif aggressiveness == "moderately aggressive":
        target_beta = (sorted_beta[2] + sorted_beta[3]) / 2
    else:
        target_beta = (sorted_beta[3] + sorted_beta[4]) / 2

    weights = ([], 0)
    while not weights[0] or any(list(map(lambda x: x <= 0, weights[0]))):
        weights, expected_rate = _get_weights(target_beta, expected_ror, beta)
        weights = [weights, calculate_higher_lower(weights, expected_rate)]
    return weights

def calculate_higher_lower(weights: list[float], expected_ror: float) -> list[float]:
    '''
    Returns the lower, expected, and upper bound on the rate of return

    Input:
    weights: weights of each company
    expected_ror: the basis of the expected rates of return

    Output:
    bounds: bounds on the rate of return, as a 68% CI
    '''
    weights = np.array(weights)
    companies = get_companies().values()
    try:
        file_name = f"{','.join(companies)}_covariance_matrix_data.json"
        file_path = os.path.join(COV_DIRECTORY, file_name)
        with open(file_path) as fp:
            data = json.load(fp)
            matrix = pandas.DataFrame(data["payload"]["RETURNS_CALCULATIONS"]["COVARIANCE(ANNUALIZED=TRUE)"]["covariance"])
            covariance_matrix = matrix.combine_first(matrix.T).values
    except:
        covariance_matrix = get_covariance_matrix(companies)
    
    portfolio_variance = weights.T @ covariance_matrix @ weights
    portfolio_std_dev = np.sqrt(portfolio_variance)
    return [float(expected_ror - Z_SCORE * portfolio_std_dev), expected_ror, float(expected_ror + Z_SCORE * portfolio_std_dev)]