import sys, os
import plotly.graph_objects as go
import numpy as np
from Portfolio_Building.get_weights import get_weights_given_aggressiveness

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

TOTAL_YEARS = 10

def _plot_value(principal: float, rate: float, aggro: str) -> None:
    """
    Plots an interactive investment value graph using the variance bands returned
    from get_weights_given_aggressiveness().
    
    Input:
    principal: Initial investment amount.
    rate: Expected rate of return.
    aggro: Risk level (e.g., "conservative", "moderately conservative", etc.).
    
    Output:
    Displays an interactive graph using Plotly.
    """

    _, target_bounds = get_weights_given_aggressiveness(aggro)
    lower_bound, expected_rate, upper_bound = target_bounds 

    t = np.arange(0, TOTAL_YEARS + 1, 1)
    A = principal * (1 + expected_rate) ** t  # Main investment growth curve

    lower_curve = principal * (1 + lower_bound) ** t
    upper_curve = principal * (1 + upper_bound) ** t

    variance_levels = [(lower_curve, upper_curve, 'rgba(173, 216, 230, 0.3)')]

    fig = go.Figure()

    # Graph the actual variance bands as they were returned
    for lower, upper, color in variance_levels:
        fig.add_trace(go.Scatter(
            x=np.concatenate((t, t[::-1])),
            y=np.concatenate((upper, lower[::-1])),
            fill='toself',
            fillcolor=color,
            line=dict(color='rgba(0, 0, 0, 0)'),
            hoverinfo="skip",
            showlegend=False
        ))

    # Main investment growth line
    fig.add_trace(go.Scatter(
        x=t, y=A,
        mode='lines',
        showlegend=False,
        line=dict(color='white', width=2),
        hovertemplate="Year: %{x}<br>Value: $%{y:,.2f}<extra></extra>"
    ))

    if aggro == "conservative":
        bg_color = "rgb(51, 153, 255)"  # Conservative (Blue)
    elif aggro == "moderately conservative":
        bg_color = "rgb(102, 204, 255)"  # Moderately Conservative (Light Blue)
    elif aggro == "moderately aggressive":
        bg_color = "rgb(255, 153, 51)"  # Moderately Aggressive (Orange)
    elif aggro == "aggressive":
        bg_color = "rgb(255, 51, 51)"  # Aggressive (Red)

    y_max = max(upper_curve) * 1.1  
    y_min = min(lower_curve) * 0.9 

    # Update layout
    fig.update_layout(
        title="Investment Growth Over Time",
        xaxis_title="Years",
        yaxis_title="Investment Value ($)",
        font=dict(family="Arial", size=14, color="black"),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.3)',
            zeroline=False,
            zerolinecolor="black",
            showline=True,
            linecolor="black",
            anchor='y',
            fixedrange=False,
            range=[0, TOTAL_YEARS],
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.3)',
            zeroline=False,
            zerolinecolor="black",
            showline=True,
            linecolor="black",
            anchor='x',
            fixedrange=False,
            range=[y_min, y_max],  
        ),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color
    )

    fig.show()


def plot_value_given_aggro_and_principal(aggro: str, principal: float) -> None:
    '''
    Plots the value of the investment dynamically given aggressiveness and principal.

    Input:
    aggro: conservative, moderately conservative, moderately aggressive, aggressive.
    principal: amount initially invested.

    Output:
    Displays an interactive graph using Plotly.
    '''
    _, target_bounds = get_weights_given_aggressiveness(aggro)
    target = target_bounds[1]
    _plot_value(principal, target, aggro)