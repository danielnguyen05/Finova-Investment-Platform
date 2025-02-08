import sys, os
import plotly.graph_objects as go
import numpy as np
from Portfolio_Building.get_weights import get_weights_given_aggressiveness

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

TOTAL_YEARS = 30

def _plot_value(principal: float, rate: float) -> None:
    """
    Plots an interactive investment value graph with multiple gradient-filled bands.

    Input:
    principal: Initial investment amount.
    rate: Expected rate of return (effective rate).

    Output:
    Displays an interactive graph with a smooth, multi-layered variance effect.
    """
    t = np.arange(0, TOTAL_YEARS + 1, 1)
    A = principal * (1 + rate) ** t  # Compound interest formula

    variance_levels = [
        (0.90, 1.10, 'rgba(173, 216, 230, 0.3)'),  # Inner
        (0.80, 1.20, 'rgba(173, 216, 230, 0.2)'),
        (0.70, 1.30, 'rgba(173, 216, 230, 0.1)'),
        (0.60, 1.40, 'rgba(173, 216, 230, 0)'),  # Outer
    ]

    fig = go.Figure()

    # Variance bands
    for lower, upper, color in variance_levels:
        fig.add_trace(go.Scatter(
            x=np.concatenate((t, t[::-1])),
            y=np.concatenate((A * upper, (A * lower)[::-1])),
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

    # Update layout for x,y axis and background
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
            fixedrange=True, 
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
            fixedrange=True, 
            range=[0, max(A) * 1.1],
        ),
        plot_bgcolor='rgb(51, 153, 255)',  # Light blue background
        paper_bgcolor='rgb(51, 153, 255)',
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
    _, target = get_weights_given_aggressiveness(aggro)
    _plot_value(principal, target)
