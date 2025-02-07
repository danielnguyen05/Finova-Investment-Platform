import sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from Portfolio_Building.get_weights import get_weights_given_aggressiveness
import numpy as np
import matplotlib.pyplot as plt

TOTAL_YEARS = 10

def _plot_value(principal: float, rate: list[float]) -> None:
    '''
    Plots the investment value according to compound interest.

    Input:
    principal: the amount that was originally invested.
    rate: list of expected, lower bound, and upper bound on rate of return, as an effective rate.

    Output:
    Image of the growth of investment saved as a .png file.
    '''
    t = np.arange(0, TOTAL_YEARS + 1, 1)
    lower = principal * (1 + rate[0]) ** t
    expected = principal * (1 + rate[1]) ** t
    upper = principal * (1 + rate[2]) ** t
    
    plt.figure(figsize=(8, 5))
    
    plt.plot(t, lower, linestyle='-', color='red', label='Lower Bound')
    plt.plot(t, expected, linestyle='-', color='blue', label='Expected Return')
    plt.plot(t, upper, linestyle='-', color='green', label='Upper Bound')

    plt.fill_between(t, lower, expected, color='red', alpha=0.3)
    plt.fill_between(t, expected, upper, color='green', alpha=0.3)
    
    plt.xlabel("Years")
    plt.ylabel("Investment Value ($)")
    plt.title("Growth of Investment vs Time")
    
    ax = plt.gca()
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["top"].set_color("none")
    ax.spines["right"].set_color("none")

    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc="upper left", bbox_to_anchor=(0.05, 1))
    plt.savefig("investment_growth_plot.png")
    plt.close()

def plot_value_given_aggro_and_principal(aggro: str, principal: float) -> None:
    '''
    Plots the value of the investment given aggressiveness and principal.

    Input:
    aggro: conservative, moderately conservative, moderately aggressive, aggressive.
    principal: amount initially invested.

    Output:
    Image of the growth of investment saved as a .png file.
    '''
    _, target = get_weights_given_aggressiveness(aggro)
    _plot_value(principal, target)