import importlib.util
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from shared.data_generation.generate import generate_operational_metrics
from shared.utils.processing import run_full_processing
from shared.utils.plotting import COLORS, SCENARIO_COLORS


def _load_modeler():
    spec = importlib.util.spec_from_file_location(
        "modeler",
        str(Path(__file__).parent / "01_scenario_modeling" / "src" / "modeler.py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@st.cache_resource
def load_data():
    raw = generate_operational_metrics()
    processed = run_full_processing(raw)
    modeler = _load_modeler()
    scenarios = modeler.run_all_scenarios(raw)
    scenario_flat = modeler.scenarios_to_flat_df(scenarios)
    scenario_summary = modeler.scenarios_endpoint_summary(scenarios)
    return raw, processed, scenarios, scenario_flat, scenario_summary


# -----------------------
# Page configuration
# -----------------------
st.set_page_config(page_title="LLM Scenario Modelling", layout="wide")

# -----------------------
# Navigation
# -----------------------
page = st.radio(
    "Select Deliverable",
    ("Scenario Modeling", "Insight Extraction", "Strategic Dashboard", "Documentation"),
    horizontal=True,
)

raw, processed, scenarios, scenario_flat, scenario_summary = load_data()
facilities = sorted(raw["facility"].unique())
metrics = sorted(raw["metric"].unique())

# -----------------------
# Deliverable 1: Scenario Modeling
# -----------------------
if page == "Scenario Modeling":
    st.title("Scenario Modeling")
    st.markdown(
        "Monte Carlo simulation engine (200 paths x 4 scenarios x 12 months) &mdash; "
        "AI-powered scenario interpretation via Claude API &mdash; "
        "Fan charts, uncertainty bands, resilience analysis"
    )

    col1, col2 = st.columns(2)
    with col1:
        selected_facility = st.selectbox("Facility", facilities, key="d1_fac")
    with col2:
        metric_labels = [m.replace("_", " ").title() for m in metrics]
        selected_label = st.selectbox("Metric", metric_labels, key="d1_met")

    metric_key = metrics[metric_labels.index(selected_label)]

    if selected_facility in scenarios and metric_key in scenarios.get(selected_facility, {}):
        fig = go.Figure()
        for sname, proj in scenarios[selected_facility][metric_key].items():
            color = SCENARIO_COLORS.get(sname, "#888")
            fig.add_trace(go.Scatter(
                x=pd.concat([proj["month"], proj["month"][::-1]]),
                y=pd.concat([proj["p90"], proj["p10"][::-1]]),
                fill="toself", fillcolor=color, opacity=0.15,
                line=dict(width=0), showlegend=False,
            ))
            fig.add_trace(go.Scatter(
                x=proj["month"], y=proj["median"], mode="lines",
                name=sname.replace("_", " ").title(),
                line=dict(color=color, width=2),
            ))
        fig.update_layout(
            template="plotly_white",
            title=f"{selected_label} — {selected_facility}",
            xaxis_title="Months Ahead",
            yaxis_title="Projected Value",
            height=500,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No scenario data available for this selection.")

    st.subheader("Endpoint Summary")
    summary_display = scenario_summary[
        (scenario_summary["facility"] == selected_facility)
        & (scenario_summary["metric"] == metric_key)
    ]
    if not summary_display.empty:
        st.dataframe(summary_display, use_container_width=True, hide_index=True)

# -----------------------
# Deliverable 2: Insight Extraction
# -----------------------
elif page == "Insight Extraction":
    st.title("Insight Extraction")
    st.markdown(
        "Analysis types: trends, anomalies, correlations, facility comparison, risk, "
        "executive summary &mdash; Structured prompt engineering for consistent AI output &mdash; "
        "Heatmaps, radar charts, anomaly timelines"
    )

    selected_facility = st.selectbox("Facility", facilities, key="d2_fac")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Correlation Heatmap")
        fac_corr = processed["correlations"]
        fac_corr = fac_corr[fac_corr["facility"] == selected_facility]
        if not fac_corr.empty:
            corr_metrics = sorted(set(fac_corr["metric_1"]) | set(fac_corr["metric_2"]))
            matrix = pd.DataFrame(1.0, index=corr_metrics, columns=corr_metrics)
            for _, row in fac_corr.iterrows():
                matrix.loc[row["metric_1"], row["metric_2"]] = row["correlation"]
                matrix.loc[row["metric_2"], row["metric_1"]] = row["correlation"]
            fig = px.imshow(
                matrix, text_auto=".2f", color_continuous_scale="RdBu_r",
                zmin=-1, zmax=1, aspect="auto",
            )
            fig.update_layout(
                template="plotly_white",
                title=f"Correlations — {selected_facility}",
                height=500,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No correlation data available.")

    with col2:
        st.subheader("Facility Comparison Radar")
        summary = processed["summary"]
        radar = summary.pivot_table(index="metric", columns="facility", values="mean")
        norm = radar.apply(
            lambda x: (x - x.min()) / (x.max() - x.min()) * 100
            if x.max() != x.min() else 50,
            axis=1,
        )
        fig = go.Figure()
        for fac in norm.columns:
            vals = norm[fac].tolist() + [norm[fac].iloc[0]]
            cats = norm.index.tolist() + [norm.index[0]]
            fig.add_trace(go.Scatterpolar(
                r=vals, theta=cats, fill="toself", name=fac, opacity=0.6,
                line=dict(color=COLORS.get(fac)),
            ))
        fig.update_layout(
            template="plotly_white", height=500,
            title="Facility Comparison (Normalized)",
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Anomaly Timeline")
    anom = processed["anomalies"]
    fac_anom = anom[anom["facility"] == selected_facility]
    if not fac_anom.empty:
        fig = px.scatter(
            fac_anom, x="date", y="z_score", color="metric",
            size=fac_anom["z_score"].abs(), height=400,
        )
        fig.add_hline(y=2, line_dash="dash", line_color="orange", opacity=0.5)
        fig.add_hline(y=-2, line_dash="dash", line_color="orange", opacity=0.5)
        fig.update_layout(
            template="plotly_white",
            title=f"Anomalies — {selected_facility}",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No anomalies detected for this facility.")

    if st.button("Extract AI Insights"):
        try:
            ext_spec = importlib.util.spec_from_file_location(
                "extractor",
                str(Path(__file__).parent / "02_insight_extraction" / "src" / "extractor.py"),
            )
            ext = importlib.util.module_from_spec(ext_spec)
            ext_spec.loader.exec_module(ext)
            with st.spinner("Querying Claude API..."):
                insights = ext.extract_all_insights(processed)
            for key, text in insights.items():
                st.subheader(key.replace("_", " ").title())
                st.write(text)
                st.divider()
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Ensure ANTHROPIC_API_KEY is set in your .env file.")

# -----------------------
# Deliverable 3: Strategic Dashboard
# -----------------------
elif page == "Strategic Dashboard":
    st.title("Strategic Dashboard")
    st.markdown(
        "Full interactive dashboard with KPI cards, trend lines, scenario projections "
        "&mdash; On-demand Claude API insights panel"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        sel_facilities = st.multiselect(
            "Facilities", facilities, default=facilities, key="d3_fac",
        )
    with col2:
        default_metrics = [
            "production_output", "quality_rate",
            "defect_rate_ppm", "on_time_delivery_pct",
        ]
        sel_metrics = st.multiselect(
            "Metrics", metrics,
            default=[m for m in default_metrics if m in metrics],
            key="d3_met",
        )
    with col3:
        months = st.slider("Time Range (months)", 3, 24, 12, step=3, key="d3_months")

    df = raw[raw["facility"].isin(sel_facilities)].copy()
    if not df.empty:
        cutoff = df["date"].max() - pd.DateOffset(months=months)
        df = df[df["date"] >= cutoff]

    # KPI Cards
    kpi_metrics = ["production_output", "quality_rate", "on_time_delivery_pct", "defect_rate_ppm"]
    kpi_cols = st.columns(len(kpi_metrics))
    for i, m in enumerate(kpi_metrics):
        mdf = df[df["metric"] == m]
        if mdf.empty:
            continue
        current = mdf.sort_values("date").groupby("facility")["value"].last().mean()
        prev = mdf.sort_values("date").groupby("facility")["value"].nth(-2).mean()
        change = ((current - prev) / prev * 100) if prev else 0
        good = change < 0 if m == "defect_rate_ppm" else change > 0
        unit = mdf["unit"].iloc[0]
        kpi_cols[i].metric(
            label=m.replace("_", " ").title(),
            value=f"{current:,.1f} {unit}",
            delta=f"{change:+.1f}% MoM",
            delta_color="normal" if good else "inverse",
        )

    st.divider()

    # Trend chart
    st.subheader("Trends")
    trend_df = df[df["metric"].isin(sel_metrics)]
    if not trend_df.empty:
        fig = px.line(
            trend_df, x="date", y="value", color="facility",
            facet_row="metric", color_discrete_map=COLORS,
            height=max(350, len(sel_metrics) * 200),
        )
        fig.update_layout(template="plotly_white")
        fig.update_yaxes(matches=None)
        fig.for_each_annotation(
            lambda a: a.update(text=a.text.split("=")[-1].replace("_", " ").title())
        )
        st.plotly_chart(fig, use_container_width=True)

    # Scenario projections
    st.subheader("Scenario Projections")
    sc_df = scenario_summary[
        scenario_summary["facility"].isin(sel_facilities)
        & scenario_summary["metric"].isin(sel_metrics)
    ]
    if not sc_df.empty:
        fig = px.bar(
            sc_df, x="metric", y="projected_median", color="scenario",
            facet_col="facility", barmode="group",
            color_discrete_map=SCENARIO_COLORS, height=400,
        )
        fig.update_layout(template="plotly_white")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    # AI insights
    if st.button("Get AI Insights", key="d3_ai"):
        try:
            ext_spec = importlib.util.spec_from_file_location(
                "extractor",
                str(Path(__file__).parent / "02_insight_extraction" / "src" / "extractor.py"),
            )
            ext = importlib.util.module_from_spec(ext_spec)
            ext_spec.loader.exec_module(ext)
            with st.spinner("Querying Claude API..."):
                insights = ext.extract_all_insights(processed)
            for key, text in insights.items():
                st.subheader(key.replace("_", " ").title())
                st.write(text)
                st.divider()
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Ensure ANTHROPIC_API_KEY is set in your .env file.")

# -----------------------
# Deliverable 4: Documentation
# -----------------------
elif page == "Documentation":
    st.title("Documentation")
    st.markdown(
        "System & AI architecture docs &mdash; Quick start guide &mdash; "
        "Interview presentation guide &mdash; Extension/training guide"
    )

    doc_path = Path(__file__).parent / "04_documentation" / "guides" / "presenting_this_project.md"
    try:
        md_content = doc_path.read_text(encoding="utf-8")
        st.markdown(md_content)
    except FileNotFoundError:
        st.warning(f"Documentation file not found at {doc_path}")

# -----------------------
# Footer
# -----------------------
st.markdown("---")
st.markdown("LLM Scenario Modelling — Streamlit Version")
