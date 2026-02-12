"""Shared Plotly helpers for consistent chart styling across deliverables."""

import plotly.graph_objects as go
import plotly.io as pio

COLORS = {
    "Plant Alpha": "#636EFA",
    "Plant Beta": "#EF553B",
    "Plant Gamma": "#00CC96",
}

SCENARIO_COLORS = {
    "optimistic": "#00CC96",
    "baseline": "#636EFA",
    "pessimistic": "#FFA15A",
    "worst_case": "#EF553B",
    "scenario 1": "#1f77b4",
    "scenario 2": "#ff7f0e",
    "scenario 3": "#2ca02c",
    "scenario 4": "#d62728",
}


def apply_portfolio_style(fig: go.Figure, title: str = "") -> go.Figure:
    """Apply consistent styling for portfolio presentation."""
    fig.update_layout(
        template="plotly_white",
        title=dict(text=title, font=dict(size=16)),
        font=dict(family="Inter, Arial, sans-serif", size=12),
        margin=dict(l=60, r=30, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0,0,0,0.05)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0,0,0,0.05)")
    return fig


def save_figure(fig: go.Figure, path: str, width: int = 1000, height: int = 500):
    """Save figure as both HTML (interactive) and PNG (static)."""
    fig.write_html(f"{path}.html", include_plotlyjs="cdn")
    try:
        fig.write_image(f"{path}.png", width=width, height=height, scale=2)
    except Exception:
        pass  # kaleido may not be available; HTML is the primary output


def fan_chart(df) -> go.Figure:
    """Create an area chart showing scenario uncertainty ranges (upper and lower bounds)."""
    import pandas as pd
    
    fig = go.Figure()
    
    # df should have scenarios as columns and dates as index
    # Display upper bound as filled area
    if isinstance(df, pd.DataFrame) and len(df.columns) > 0:
        for scenario in df.columns:
            color = SCENARIO_COLORS.get(scenario.lower(), "#636EFA")
            
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df[scenario],
                mode="lines",
                name=scenario.replace("_upper", "").replace("_lower", ""),
                line=dict(color=color, width=1),
                opacity=0,
                hoverinfo="skip",
            ))
    
    # Add filled areas for upper bounds
    scenario_nums = set([col.replace("_upper", "").replace("_lower", "") for col in df.columns])
    
    for scenario in sorted(scenario_nums):
        if f"{scenario}_upper" in df.columns:
            color = SCENARIO_COLORS.get(scenario.lower(), "#636EFA")
            
            fig.add_trace(go.Scatter(
                x=df.index.tolist() + df.index.tolist()[::-1],
                y=df[f"{scenario}_upper"].tolist() + df[f"{scenario}_lower"].tolist()[::-1],
                fill="toself",
                fillcolor=color,
                opacity=0.2,
                line=dict(color="rgba(0,0,0,0)"),
                name=f"{scenario} range",
                hoverinfo="skip",
                showlegend=False,
            ))
    
    return apply_portfolio_style(fig, "Scenario Uncertainty Ranges")
