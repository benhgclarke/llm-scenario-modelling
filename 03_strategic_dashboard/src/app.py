"""Strategic Interpretation Dashboard — Plotly Dash application.

Interactive dashboard combining all deliverables: KPI overview, trend charts,
scenario projections, anomaly detection, correlations, and AI insights panel.
"""

import os
import sys
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from shared.data_generation.generate import generate_operational_metrics, save_data
from shared.utils.processing import run_full_processing
from shared.utils.plotting import COLORS, SCENARIO_COLORS

# ── Data initialization ───────────────────────────────────────────────────

def _load_modeler():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "modeler",
        str(Path(__file__).parent.parent.parent / "01_scenario_modeling" / "src" / "modeler.py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def init_data():
    data_dir = Path(__file__).parent.parent / "data"
    csv_path = data_dir / "operational_metrics.csv"

    if csv_path.exists():
        raw = pd.read_csv(csv_path, parse_dates=["date"])
    else:
        raw = generate_operational_metrics()
        save_data(raw, str(data_dir))

    processed = run_full_processing(raw)

    modeler = _load_modeler()
    scenarios = modeler.run_all_scenarios(raw)
    scenario_summary = modeler.scenarios_endpoint_summary(scenarios)
    scenario_flat = modeler.scenarios_to_flat_df(scenarios)

    return raw, processed, scenarios, scenario_summary, scenario_flat


RAW_DF, PROCESSED, SCENARIOS, SCENARIO_SUMMARY, SCENARIO_FLAT = init_data()

# ── App ───────────────────────────────────────────────────────────────────

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    title="AI Operational Analytics Dashboard",
    suppress_callback_exceptions=True,
)

FACILITIES = sorted(RAW_DF["facility"].unique())
METRICS = sorted(RAW_DF["metric"].unique())

# ── Sidebar ───────────────────────────────────────────────────────────────

sidebar = dbc.Card([
    html.H5("Filters", className="mb-3"),
    html.Label("Facility"),
    dcc.Dropdown(
        id="facility-filter",
        options=[{"label": f, "value": f} for f in FACILITIES],
        value=FACILITIES,
        multi=True,
    ),
    html.Label("Metric", className="mt-3"),
    dcc.Dropdown(
        id="metric-filter",
        options=[{"label": m.replace("_", " ").title(), "value": m} for m in METRICS],
        value=["production_output", "quality_rate", "defect_rate_ppm", "on_time_delivery_pct"],
        multi=True,
    ),
    html.Label("Time Range (months)", className="mt-3"),
    dcc.Slider(
        id="time-range", min=3, max=24, step=3, value=12,
        marks={i: str(i) for i in range(3, 25, 3)},
    ),
    html.Hr(),
    html.H5("AI Analysis", className="mb-3"),
    dbc.Button("Generate Insights", id="btn-insights", color="primary", className="w-100 mb-2"),
    dbc.Button("Run Scenario Analysis", id="btn-scenarios", color="info", className="w-100"),
], body=True, className="h-100")

# ── Main content ──────────────────────────────────────────────────────────

main_content = html.Div([
    # KPI cards
    html.Div(id="kpi-cards", className="mb-4"),

    # Tabs for different views
    dbc.Tabs([
        dbc.Tab(label="Trends", children=[
            dcc.Graph(id="trend-chart", className="mt-3"),
        ]),
        dbc.Tab(label="Scenarios", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id="scenario-bar-chart"), md=6),
                dbc.Col(dcc.Graph(id="scenario-fan-chart"), md=6),
            ], className="mt-3"),
        ]),
        dbc.Tab(label="Anomalies", children=[
            dcc.Graph(id="anomaly-chart", className="mt-3"),
        ]),
        dbc.Tab(label="Correlations", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id="correlation-heatmap"), md=6),
                dbc.Col(dcc.Graph(id="facility-radar"), md=6),
            ], className="mt-3"),
        ]),
        dbc.Tab(label="AI Insights", children=[
            dbc.Card([
                dcc.Loading(html.Div(
                    id="ai-insights-panel",
                    children="Click 'Generate Insights' to get AI-powered analysis.",
                    style={"whiteSpace": "pre-wrap", "maxHeight": "600px", "overflowY": "auto"},
                )),
            ], body=True, className="mt-3"),
        ]),
    ]),
])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H3("AI-Enhanced Operational Analytics", className="my-3"), md=8),
        dbc.Col(html.Div([
            dbc.Badge("Powered by Claude API", color="primary", className="me-1"),
            dbc.Badge("Portfolio Project", color="secondary"),
        ], className="float-end mt-3"), md=4),
    ]),
    dbc.Row([
        dbc.Col(sidebar, md=3),
        dbc.Col(main_content, md=9),
    ]),
], fluid=True, className="py-3")

# ── Callbacks ─────────────────────────────────────────────────────────────

@callback(Output("kpi-cards", "children"), Input("facility-filter", "value"), Input("time-range", "value"))
def update_kpi_cards(facilities, months):
    df = RAW_DF[RAW_DF["facility"].isin(facilities)]
    cutoff = df["date"].max() - pd.DateOffset(months=months)
    df = df[df["date"] >= cutoff]

    kpi_metrics = ["production_output", "quality_rate", "on_time_delivery_pct", "defect_rate_ppm"]
    cards = []
    for m in kpi_metrics:
        mdf = df[df["metric"] == m]
        if mdf.empty:
            continue
        current = mdf.sort_values("date").groupby("facility")["value"].last().mean()
        prev = mdf.sort_values("date").groupby("facility")["value"].nth(-2).mean()
        change = ((current - prev) / prev * 100) if prev else 0
        good = change < 0 if m == "defect_rate_ppm" else change > 0
        color = "success" if good else "danger"
        arrow = "+" if change > 0 else ""
        unit = mdf["unit"].iloc[0]

        cards.append(dbc.Col(dbc.Card([
            html.H6(m.replace("_", " ").title(), className="text-muted mb-1", style={"fontSize": "0.8rem"}),
            html.H4(f"{current:,.1f} {unit}"),
            html.Span(f"{arrow}{change:.1f}% MoM", className=f"text-{color}"),
        ], body=True), md=3))

    return dbc.Row(cards)


@callback(Output("trend-chart", "figure"), Input("facility-filter", "value"), Input("metric-filter", "value"), Input("time-range", "value"))
def update_trend_chart(facilities, metrics, months):
    df = RAW_DF[RAW_DF["facility"].isin(facilities) & RAW_DF["metric"].isin(metrics)]
    cutoff = df["date"].max() - pd.DateOffset(months=months)
    df = df[df["date"] >= cutoff]

    fig = px.line(
        df, x="date", y="value", color="facility", facet_row="metric",
        color_discrete_map=COLORS, height=max(350, len(metrics) * 200),
    )
    fig.update_layout(template="plotly_white", margin=dict(l=60, r=20, t=30, b=30))
    fig.update_yaxes(matches=None)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1].replace("_", " ").title()))
    return fig


@callback(Output("scenario-bar-chart", "figure"), Input("facility-filter", "value"), Input("metric-filter", "value"))
def update_scenario_bar(facilities, metrics):
    df = SCENARIO_SUMMARY[SCENARIO_SUMMARY["facility"].isin(facilities) & SCENARIO_SUMMARY["metric"].isin(metrics)]
    if df.empty:
        return go.Figure().update_layout(template="plotly_white", title="Select metrics")

    fig = px.bar(
        df, x="metric", y="projected_median", color="scenario",
        facet_col="facility", barmode="group",
        color_discrete_map=SCENARIO_COLORS, height=400,
    )
    fig.update_layout(template="plotly_white", margin=dict(l=50, r=20, t=40, b=30))
    fig.update_xaxes(tickangle=45)
    return fig


@callback(Output("scenario-fan-chart", "figure"), Input("facility-filter", "value"), Input("metric-filter", "value"))
def update_scenario_fan(facilities, metrics):
    if not facilities or not metrics:
        return go.Figure().update_layout(template="plotly_white")

    fac, met = facilities[0], metrics[0]
    if fac not in SCENARIOS or met not in SCENARIOS.get(fac, {}):
        return go.Figure().update_layout(template="plotly_white", title="No data")

    fig = go.Figure()
    for sname, proj in SCENARIOS[fac][met].items():
        color = SCENARIO_COLORS.get(sname, "#888")
        fig.add_trace(go.Scatter(
            x=pd.concat([proj["month"], proj["month"][::-1]]),
            y=pd.concat([proj["p90"], proj["p10"][::-1]]),
            fill="toself", fillcolor=color, opacity=0.15,
            line=dict(width=0), showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=proj["month"], y=proj["median"], mode="lines",
            name=sname.replace("_", " ").title(), line=dict(color=color, width=2),
        ))

    fig.update_layout(
        template="plotly_white", height=400,
        title=f"{met.replace('_', ' ').title()} — {fac}",
        xaxis_title="Months Ahead", yaxis_title="Projected Value",
    )
    return fig


@callback(Output("anomaly-chart", "figure"), Input("facility-filter", "value"))
def update_anomaly_chart(facilities):
    anom = PROCESSED["anomalies"]
    df = anom[anom["facility"].isin(facilities)]
    if df.empty:
        return go.Figure().update_layout(template="plotly_white", title="No anomalies detected")

    fig = px.scatter(
        df, x="date", y="z_score", color="facility", symbol="metric",
        size=df["z_score"].abs(), color_discrete_map=COLORS, height=400,
    )
    fig.add_hline(y=2, line_dash="dash", line_color="orange", opacity=0.5)
    fig.add_hline(y=-2, line_dash="dash", line_color="orange", opacity=0.5)
    fig.update_layout(template="plotly_white")
    return fig


@callback(Output("correlation-heatmap", "figure"), Input("facility-filter", "value"))
def update_heatmap(facilities):
    if not facilities:
        return go.Figure().update_layout(template="plotly_white")

    fac = facilities[0]
    fac_corr = PROCESSED["correlations"][PROCESSED["correlations"]["facility"] == fac]
    if fac_corr.empty:
        return go.Figure().update_layout(template="plotly_white")

    metrics = sorted(set(fac_corr["metric_1"]) | set(fac_corr["metric_2"]))
    matrix = pd.DataFrame(1.0, index=metrics, columns=metrics)
    for _, row in fac_corr.iterrows():
        matrix.loc[row["metric_1"], row["metric_2"]] = row["correlation"]
        matrix.loc[row["metric_2"], row["metric_1"]] = row["correlation"]

    fig = px.imshow(matrix, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
    fig.update_layout(template="plotly_white", title=f"Correlations — {fac}", height=450)
    return fig


@callback(Output("facility-radar", "figure"), Input("facility-filter", "value"))
def update_radar(facilities):
    summary = PROCESSED["summary"]
    df = summary[summary["facility"].isin(facilities)]
    if df.empty:
        return go.Figure().update_layout(template="plotly_white")

    radar = df.pivot_table(index="metric", columns="facility", values="mean")
    norm = radar.apply(lambda x: (x - x.min()) / (x.max() - x.min()) * 100 if x.max() != x.min() else 50, axis=1)

    fig = go.Figure()
    for fac in norm.columns:
        vals = norm[fac].tolist() + [norm[fac].iloc[0]]
        cats = norm.index.tolist() + [norm.index[0]]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=cats, fill="toself", name=fac, opacity=0.6,
            line=dict(color=COLORS.get(fac)),
        ))

    fig.update_layout(
        template="plotly_white", height=450, title="Facility Comparison (Normalized)",
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    )
    return fig


@callback(Output("ai-insights-panel", "children"), Input("btn-insights", "n_clicks"), prevent_initial_call=True)
def generate_insights(n_clicks):
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "extractor",
            str(Path(__file__).parent.parent.parent / "02_insight_extraction" / "src" / "extractor.py"),
        )
        ext = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ext)

        insights = ext.extract_all_insights(PROCESSED)
        sections = []
        for key, text in insights.items():
            sections.extend([
                html.H6(key.replace("_", " ").title(), className="text-primary mt-3"),
                html.P(text, style={"fontSize": "0.9rem"}),
                html.Hr(),
            ])
        return html.Div(sections)
    except Exception as e:
        return html.Div([
            html.P(f"Error: {e}", className="text-danger"),
            html.P("Ensure ANTHROPIC_API_KEY is set in your .env file."),
        ])


def run_dashboard():
    port = int(os.getenv("DASH_PORT", "8050"))
    debug = os.getenv("DASH_DEBUG", "true").lower() == "true"
    print(f"Dashboard starting at http://localhost:{port}")
    app.run(debug=debug, port=port)


if __name__ == "__main__":
    run_dashboard()
