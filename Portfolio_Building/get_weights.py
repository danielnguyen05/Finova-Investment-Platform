import sys, os
from random import randint
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, value, PULP_CBC_CMD

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from Portfolio_Building.get_variables import get_variables

COMPANY_COUNT = 5

def _get_weights(threshold: float, expected_ror: list[float], beta: list[float]) -> list[float]:
    '''
    Gets the weights associated with each company, listed in the file get_variables.py.

    Input:
    threshold: the required rate of return for the portfolio that has to be met
    expected_ror: list of expected rates of returns for a few given companies
    beta: list of beta for a few given companies

    Output:
    List of floats detailing what weights should be assigned to each company, as a percentage.
    '''
    problem = LpProblem("Minimize_Beta_Given_ExRoR", LpMinimize)
    weights = [LpVariable(f"w_{i+1}", lowBound=randint(1, 5)/100, upBound=randint(37, 43)/100) for i in range(COMPANY_COUNT)]
    problem += lpSum(weights) == 1
    problem += lpSum(weights[i] * expected_ror[i] for i in range(COMPANY_COUNT)) == threshold
    problem += lpSum(weights[i] * beta[i] for i in range(5))
    problem.solve(PULP_CBC_CMD(msg=False))
    weights = [round(value(i) * 100, 2) for i in weights]
    return weights

def get_weights_given_aggressiveness(aggressiveness: str) -> tuple[list[float], float]:
    '''
    Returns the appropriate weights for the given companies for a certain level of aggressiveness.

    Input:
    aggressiveness: conservative, moderately conservative, moderately aggressive, aggressive.

    Output:
    Tuple of list of floats detailing what weights should be assigned to each company, as well as a float
    which says what the target expected rate of return is.
    '''
    to_be_processed = sorted(get_variables())
    expected_ror, beta = [elem[0] for elem in to_be_processed], [elem[1] for elem in to_be_processed]
    if aggressiveness == "conservative":
        target_ror = (expected_ror[0] + expected_ror[1]) / 2
        return (_get_weights(target_ror, expected_ror, beta), target_ror)
    elif aggressiveness == "moderately conservative":
        target_ror = (expected_ror[1] + expected_ror[2]) / 2
        return (_get_weights(target_ror, expected_ror, beta), target_ror)
    elif aggressiveness == "moderately aggressive":
        target_ror = (expected_ror[2] + expected_ror[3]) / 2
        return (_get_weights(target_ror, expected_ror, beta), target_ror)
    else:
        target_ror = (expected_ror[3] + expected_ror[4]) / 2 - 0.01
        return (_get_weights(target_ror, expected_ror, beta), target_ror)