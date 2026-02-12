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
    """Create a fan chart showing scenario paths with uncertainty bands."""
    import pandas as pd
    
    fig = go.Figure()
    
    # Extract unique scenarios and paths
    if "scenario" in df.columns:
        for scenario in df["scenario"].unique():
            scenario_data = df[df["scenario"] == scenario]
            color = SCENARIO_COLORS.get(scenario.lower(), "#636EFA")
            
            for path in scenario_data["path"].unique() if "path" in scenario_data.columns else [0]:
                path_data = scenario_data[scenario_data["path"] == path] if "path" in scenario_data.columns else scenario_data
                path_data = path_data.sort_values("date") if "date" in path_data.columns else path_data
                
                fig.add_trace(go.Scatter(
                    x=path_data.get("date", list(range(len(path_data)))),
                    y=path_data["value"],
                    mode="lines",
                    name=scenario,
                    line=dict(color=color, width=1),
                    opacity=0.3,
                    legendgroup=scenario,
                    hoverinfo="skip",
                ))
    
    return apply_portfolio_style(fig, "Scenario Fan Chart")
