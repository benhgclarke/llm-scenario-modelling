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
        "description": "",
    },
    "Deliverable 3": {
        "title": "Strategic Dashboard",
        "description": "",
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
        
        # Create fixed, non-zoomable chart
        fig = go.Figure()
        scenario_colors = {
            "Scenario 1": "#1f77b4",
            "Scenario 2": "#ff7f0e",
            "Scenario 3": "#2ca02c",
            "Scenario 4": "#d62728",
        }
        for scenario in scenario_df.columns:
            fig.add_trace(go.Scatter(
                x=scenario_df.index,
                y=scenario_df[scenario],
                mode="lines",
                name=scenario,
                line=dict(color=scenario_colors.get(scenario, "#636EFA"), width=2),
            ))
        fig.update_layout(
            template="plotly_white",
            xaxis=dict(fixedrange=True),
            yaxis=dict(fixedrange=True),
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.caption("📈 Each line represents the average trajectory for each scenario over 12 months.")
    except Exception as e:
        st.error(f"Error generating scenario data: {e}")


def show_insight_extraction() -> None:
    """Display Insight Extraction deliverable."""
    st.title("Deliverable 2: Insight Extraction")
    st.markdown(DELIVERABLES["Deliverable 2"]["description"])

    st.markdown("""
    ### What This Does
    
    Once you have the data, the next question is: **What does it mean?** This section automatically analyses your operational 
    performance and highlights what's working well and what needs attention.
    
    **How It Analyses Your Data:**
    - **Performance Heatmap**: See at a glance which facilities and departments are performing best and worst
    - **Radar Chart**: Compare your facility's performance across key operational areas
    - **Trend Analysis**: Understand if performance is improving, declining or staying stable
    - **Anomaly Detection**: Get alerted to unusual spikes or drops that might indicate problems
    - **Correlations**: Discover which metrics move together (e.g., does equipment uptime affect production?)
    
    **Why This Matters:** By automatically surfacing insights, you can:
    - Quickly identify your top and bottom performers
    - Spot problems before they become serious
    - Understand which improvements will have the biggest impact
    """)

    try:
        st.subheader("Performance Heatmap")
        heatmap_data = processing.generate_heatmap_data()
        fig = px.imshow(
            heatmap_data,
            text_auto=True,
            aspect="auto",
            color_continuous_scale=[[0, "#D9F0D0"], [1, "#064E0C"]],
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("� Green indicates strong performance, white shows weaker areas. Use this to identify which departments need support.")

        st.subheader("Performance Radar Chart")
        radar_data = processing.generate_radar_data()
        fig = px.line_polar(
            radar_data, r="value", theta="metric", line_close=True
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("⭐ The shape of this chart shows where you excel and where to focus improvement efforts. A balanced pentagon = well-rounded performance.")
    except Exception as e:
        st.error(f"Error generating insight data: {e}")


def show_strategic_dashboard() -> None:
    """Display Strategic Dashboard deliverable."""
    st.title("Deliverable 3: Strategic Dashboard")
    st.markdown(DELIVERABLES["Deliverable 3"]["description"])

    st.markdown("""
    ### What This Does
    
    **The Challenge:** As a leader, you need to make quick decisions based on current business performance. But wading through 
    spreadsheets and reports takes too long. You need the critical numbers **right now**, in one place.
    
    **The Solution:** This dashboard brings together everything you need to know about your business performance in one view. 
    Think of it as your business's "health monitor" - like a dashboard in a car showing speed, fuel, engine temp all at once.
    
    **What You'll See:**
    
    1. **Financial Metrics**: Revenue and cost performance - the bottom line results
    2. **Operational Metrics**: Facility-by-facility breakdown showing which plants are performing well
    3. **Risk Indicators**: Early warning signs that something needs attention
    
    **How to Use It:**
    - **Quick Health Check**: Glance at the KPIs to see if everything is normal
    - **Spot Trends**: Compare performance across facilities to identify leaders and laggards
    - **Deep Dive**: Get AI-powered insights that explain what's driving the numbers
    
    **Why This Matters:** Instead of waiting for monthly reports, you get real-time visibility into business performance. 
    This lets you respond quickly to problems and capitalize on opportunities.
    """)

    try:
        st.subheader("Key Performance Indicators")
        kpi_values = processing.generate_kpis()
        col1, col2, col3 = st.columns(3)
        col1.metric("Revenue", f"£{kpi_values['revenue']:,}")
        col2.metric("Cost", f"£{kpi_values['cost']:,}")
        risk_score = kpi_values['risk_score']
        max_risk_score = 5  # Change if your scale is different
        col3.metric("Risk Score", f"{risk_score:.2f}/{max_risk_score}")
        st.caption("💰 These are your top 3 strategic metrics. Revenue and Cost drive profitability; Risk Score indicates operational health (out of 5).")

        st.subheader("Facility Comparison")
        df_dashboard = generate.generate_dashboard_data()
        fig = px.bar(
            df_dashboard, x="facility", y="value", color="value",
            color_continuous_scale=[[0, "#4A90E2"], [1, "#003D99"]],
            title="Revenue by Facility"
        )
        fig.update_layout(coloraxis_colorbar=dict(title="Value"))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("🏭 This bar chart compares revenue performance across your three plants. Darker blue = higher revenue generation.")
    except Exception as e:
        st.error(f"Error generating dashboard: {e}")


def show_documentation() -> None:
    """Display Documentation deliverable."""
    st.title("Deliverable 4: Documentation")
    st.markdown("""
    ### What This Is

    This section provides complete documentation covering the entire system, including:

    - **System Architecture:** Explains how all the components of the platform work together, from data generation to dashboard visualisation.
    - **AI Integration Guide:** Details how the Claude API is used to power automated insights and how you can configure or extend this integration.
    - **Quick Start Guide:** Step-by-step instructions to get the system up and running in just five minutes, suitable for both technical and non-technical users.
    - **Presentation Guide:** Tips and resources for presenting this project to stakeholders, including suggested talking points and visual aids.
    - **Extension Guide:** Guidance on how to build on top of this system, whether you want to add new data sources, analytics or visualisations.

    This documentation provides everything needed to understand, maintain and scale the system effectively.
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
    "Scenario Modeling": show_scenario_modeling,
    "Insight Extraction": show_insight_extraction,
    "Strategic Dashboard": show_strategic_dashboard,
    "Documentation": show_documentation,
}


def main() -> None:
    """Main app entry point."""
    st.sidebar.markdown("# 📊 LLM Scenario Modelling")
    st.sidebar.markdown("""Turn your operations data into smart business decisions. Explore multiple future scenarios and get AI-powered recommendations to drive better results.""")
    st.sidebar.markdown("---")
    
    deliverable = st.sidebar.radio(
        "Select Section",
        list(DELIVERABLE_VIEWS.keys()),
    )

    DELIVERABLE_VIEWS[deliverable]()

    # -----------------------
    # Footer
    # -----------------------
    st.markdown("---")
    st.markdown("LLM Scenario Modelling — Streamlit Version")


if __name__ == "__main__":
    main()
