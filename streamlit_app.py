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
        "description": "",
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

    st.markdown("""
    ### What This Does
    
    **The Challenge:** In business, the future is uncertain. Should you invest in new equipment? Will demand grow or shrink? 
    Instead of guessing, we use data science to explore multiple possible futures.

    **How It Works:**
    This tool uses a technique called **scenario modeling** to show you different possible futures for your business. 
    Think of it like a weather forecast that shows multiple possible outcomes (sunny, rainy, snowy) instead of just one prediction.
    
    **Three Key Concepts:**
    
    1. **Scenarios**: We model 4 different business conditions:
       - **Scenario 1 (Conservative)**: Things improve slowly - cautious growth
       - **Scenario 2 (Baseline)**: Business continues as normal - steady performance
       - **Scenario 3 (Optimistic)**: Things improve noticeably - strong growth
       - **Scenario 4 (Aggressive)**: Major changes happen - rapid transformation
    
    2. **Uncertainty Bands**: For each scenario, we run 200 different simulations (think of them as 200 different possible timelines). 
       This shows us not just the "average" outcome, but the range of what could happen. Some timelines might do better, 
       some worse - that's the uncertainty.
    
    3. **12-Month Horizon**: We project forward 12 months (one year) to see how each scenario plays out over time.

    **Why This Matters:** By seeing multiple possible futures, you can:
    - Prepare for different outcomes instead of being surprised
    - Identify which scenarios matter most to your business
    - Make better decisions about investments and strategy
    """)

    try:
        scenario_df = generate.generate_scenarios(
            n_paths=SIMULATOR_CONFIG["n_paths"],
            n_months=SIMULATOR_CONFIG["n_months"],
            n_scenarios=SIMULATOR_CONFIG["n_scenarios"],
        )
        st.subheader("Scenario Projections")
        st.line_chart(scenario_df)
        st.caption("📈 Each line represents the average trajectory for each scenario over 12 months.")

        fig = plotting.fan_chart(scenario_df)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("📊 **Uncertainty Bands**: This view shows the same scenarios with thicker bands to represent the uncertainty and range in possible outcomes. Wider gaps between scenarios = greater divergence in outcomes.")
    except Exception as e:
        st.error(f"Error generating scenario data: {e}")


def show_insight_extraction() -> None:
    """Display Insight Extraction deliverable."""
    st.title("Deliverable 2: Insight Extraction")
    st.markdown(DELIVERABLES["Deliverable 2"]["description"])

    st.markdown("""
    ### What This Does
    This section analyzes operational data across multiple dimensions to surface key insights. 
    We examine 10 different KPIs across 3 manufacturing plants using 6 different analysis approaches:

    **6 Analysis Types:**
    1. **Trends**: How are KPIs moving over time?
    2. **Anomalies**: Are there unusual spikes or dips?
    3. **Correlations**: Which KPIs move together?
    4. **Facility Comparison**: Which plant performs best?
    5. **Risk Analysis**: Where are the biggest operational risks?
    6. **Executive Summary**: AI-generated insights in plain English
    """)

    try:
        st.subheading("Performance Heatmap")
        heatmap_data = processing.generate_heatmap_data()
        fig = px.imshow(
            heatmap_data,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Viridis",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("🔥 Heatmap shows performance scores (0-100) across facilities and key metrics. Darker = better performance.")

        st.subheading("Performance Radar Chart")
        radar_data = processing.generate_radar_data()
        fig = px.line_polar(
            radar_data, r="value", theta="metric", line_close=True
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("📊 Radar chart compares your facility across 5 operational dimensions. Larger area = better overall performance.")
    except Exception as e:
        st.error(f"Error generating insight data: {e}")


def show_strategic_dashboard() -> None:
    """Display Strategic Dashboard deliverable."""
    st.title("Deliverable 3: Strategic Dashboard")
    st.markdown(DELIVERABLES["Deliverable 3"]["description"])

    st.markdown("""
    ### What This Does
    This is a real-time **executive dashboard** showing the most critical KPIs at a glance. 
    It combines financial metrics, operational health, and risk indicators to give leadership 
    a comprehensive view of business performance. All data is interactive and can be used to 
    drill down into specific areas.
    """)

    try:
        st.subheading("Key Performance Indicators")
        kpi_values = processing.generate_kpis()
        col1, col2, col3 = st.columns(3)
        col1.metric("Revenue", f"${kpi_values['revenue']:,}")
        col2.metric("Cost", f"${kpi_values['cost']:,}")
        col3.metric("Risk Score", f"{kpi_values['risk_score']:.2f}")
        st.caption("💰 These are your top 3 strategic metrics. Revenue and Cost drive profitability; Risk Score indicates operational health.")

        st.subheading("Facility Comparison")
        df_dashboard = generate.generate_dashboard_data()
        fig = px.bar(
            df_dashboard, x="facility", y="value", color="value",
            color_continuous_scale=[[0, "#4A90E2"], [1, "#003D99"]],
            title="Revenue by Facility"
        )
        fig.update_layout(coloraxis_colorbar=dict(title="Value"))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("🏭 This bar chart compares revenue performance across your three plants. Darker blue = higher revenue generation.")

        st.markdown("---")
        st.markdown("### AI-Powered Insights Panel")
        st.markdown("Ask Claude AI to analyze the data above and generate strategic recommendations.")
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

    st.markdown("""
    ### What This Is
    Complete documentation covering the entire system, including:
    - **System Architecture**: How all components work together
    - **AI Integration Guide**: How Claude API powers the insights
    - **Quick Start Guide**: Getting up and running in 5 minutes
    - **Presentation Guide**: How to present this project to stakeholders
    - **Extension Guide**: How to build on top of this system

    This section provides everything needed to understand, maintain, and scale the system.
    """)

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
    st.sidebar.markdown("# 📊 LLM Scenario Modelling")
    st.sidebar.markdown("""
    An AI-augmented analytics system for manufacturing operations. 
    Combines statistical analysis, Monte Carlo simulation, and Claude API insights.
    """)
    st.sidebar.markdown("---")
    
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
