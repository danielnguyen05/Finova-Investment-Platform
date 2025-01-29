import sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from Portfolio_Building.get_weights import get_weights_given_aggressiveness
import numpy as np
import matplotlib.pyplot as plt

TOTAL_YEARS = 30

def _plot_value(principal: float, rate: float) -> None:
    '''
    Plots the investment value according to compound interest.

    Input:
    principal: the amount that was originally invested.
    rate: expected rate of return, as an effective rate.

    Output:
    Image of the growth of investment saved as a .png file.
    '''
    t = np.arange(0, TOTAL_YEARS + 1, 1)
    A = principal * (1 + rate) ** t
    
    plt.figure(figsize=(8, 5))
    plt.plot(t, A, linestyle='-', color='blue')

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
    return None