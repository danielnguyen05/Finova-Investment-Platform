import sys, os
from pulp import LpProblem, LpVariable, lpSum, LpMaximize, value, PULP_CBC_CMD
from random import randint

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from Portfolio_Building.get_variables import get_variables

COMPANY_COUNT = 5

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
    weights = [round(value(w) * 100, 2) for w in weights]
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
        weights = _get_weights(target_beta, expected_ror, beta)
    return weights