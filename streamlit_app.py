import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from shared.data_generation import generate
from shared.utils import processing, plotting, llm_client

# -----------------------
# Constants & Configuration
# -----------------------
PAGE_CONFIG = {
    "page_title": "LLM Scenario Modelling",
    "layout": "wide",
}

DELIVERABLES = {
    "Deliverable 1": {
        "title": "Scenario Modeling",
        "description": "Monte Carlo simulation engine (200 paths × 4 scenarios × 12 months)\nAI-powered scenario interpretation via Claude API\nFan charts, uncertainty bands, resilience analysis",
    },
    "Deliverable 2": {
        "title": "Insight Extraction",
        "description": "Analysis types: trends, anomalies, correlations, facility comparison, risk, executive summary\nStructured prompt engineering for consistent AI output\nHeatmaps, radar charts, anomaly timelines",
    },
    "Deliverable 3": {
        "title": "Strategic Dashboard",
        "description": "Full Plotly dashboard with tabbed interface, KPI cards, filtering\nOn-demand Claude API insights panel",
    },
    "Deliverable 4": {
        "title": "Documentation",
        "description": "System & AI architecture docs\nQuick start guide\nInterview presentation guide\nExtension/training guide",
    },
}

SIMULATOR_CONFIG = {
    "n_paths": 200,
    "n_months": 12,
    "n_scenarios": 4,
}

DOCUMENTATION_PATH = "04_documentation/guides/presenting_this_project.md"

# -----------------------
# Page Setup
# -----------------------
st.set_page_config(**PAGE_CONFIG)

# -----------------------
# Deliverable Functions
# -----------------------
def show_scenario_modeling() -> None:
    """Display Scenario Modeling deliverable."""
    st.title("Deliverable 1: Scenario Modeling")
    st.markdown(DELIVERABLES["Deliverable 1"]["description"])

    try:
        scenario_df = generate.generate_scenarios(
            n_paths=SIMULATOR_CONFIG["n_paths"],
            n_months=SIMULATOR_CONFIG["n_months"],
            n_scenarios=SIMULATOR_CONFIG["n_scenarios"],
        )
        st.line_chart(scenario_df)

        fig = plotting.fan_chart(scenario_df)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error generating scenario data: {e}")


def show_insight_extraction() -> None:
    """Display Insight Extraction deliverable."""
    st.title("Deliverable 2: Insight Extraction")
    st.markdown(DELIVERABLES["Deliverable 2"]["description"])

    try:
        heatmap_data = processing.generate_heatmap_data()
        fig = px.imshow(
            heatmap_data,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Viridis",
        )
        st.plotly_chart(fig, use_container_width=True)

        radar_data = processing.generate_radar_data()
        fig = px.line_polar(
            radar_data, r="value", theta="metric", line_close=True
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error generating insight data: {e}")


def show_strategic_dashboard() -> None:
    """Display Strategic Dashboard deliverable."""
    st.title("Deliverable 3: Strategic Dashboard")
    st.markdown(DELIVERABLES["Deliverable 3"]["description"])

    try:
        kpi_values = processing.generate_kpis()
        col1, col2, col3 = st.columns(3)
        col1.metric("Revenue", f"${kpi_values['revenue']:,}")
        col2.metric("Cost", f"${kpi_values['cost']:,}")
        col3.metric("Risk Score", f"{kpi_values['risk_score']:.2f}")

        df_dashboard = generate.generate_dashboard_data()
        fig = px.bar(
            df_dashboard, x="facility", y="value", color="value",
            color_continuous_scale=[[0, "#E8F1F9"], [1, "#003D99"]],
            title="Revenue by Facility"
        )
        fig.update_layout(coloraxis_colorbar=dict(title="Value"))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown("### AI Insights Panel")
        if st.button("Get AI Insights"):
            with st.spinner("Generating insights..."):
                insights = llm_client.get_insights(df_dashboard)
                if "Unable to generate insights" in insights:
                    st.warning(
                        "🔑 **API Key Required**\n\n"
                        "To enable AI insights, add your Anthropic API key:\n\n"
                        "1. Copy `.env.example` to `.env`\n"
                        "2. Add your `ANTHROPIC_API_KEY`\n"
                        "3. Restart the app"
                    )
                else:
                    st.success("Insights Generated")
                    st.write(insights)
    except Exception as e:
        st.error(f"Error generating dashboard: {e}")


def show_documentation() -> None:
    """Display Documentation deliverable."""
    st.title("Deliverable 4: Documentation")
    st.markdown(DELIVERABLES["Deliverable 4"]["description"])

    try:
        doc_file = Path(DOCUMENTATION_PATH)
        if doc_file.exists():
            with open(doc_file, "r", encoding="utf-8") as f:
                md_content = f.read()
            st.markdown(md_content)
        else:
            st.warning(f"Documentation file not found at {DOCUMENTATION_PATH}")
    except Exception as e:
        st.error(f"Error loading documentation: {e}")


# -----------------------
# Router
# -----------------------
DELIVERABLE_VIEWS = {
    "Deliverable 1": show_scenario_modeling,
    "Deliverable 2": show_insight_extraction,
    "Deliverable 3": show_strategic_dashboard,
    "Deliverable 4": show_documentation,
}


def main() -> None:
    """Main app entry point."""
    deliverable = st.radio(
        "Select Deliverable",
        list(DELIVERABLES.keys()),
    )

    DELIVERABLE_VIEWS[deliverable]()

    # -----------------------
    # Footer
    # -----------------------
    st.markdown("---")
    st.markdown("LLM Scenario Modelling — Streamlit Version")


if __name__ == "__main__":
    main()
