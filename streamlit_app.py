import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from shared import data_generator, processing, plotting, llm_client

# -----------------------
# Page configuration
# -----------------------
st.set_page_config(
    page_title="LLM Scenario Modelling",
    layout="wide",
)

# -----------------------
# Navigation menu
# -----------------------
deliverable = st.radio(
    "Select Deliverable",
    ("Deliverable 1", "Deliverable 2", "Deliverable 3", "Deliverable 4")
)

# -----------------------
# Deliverable 1: Scenario Modeling
# -----------------------
if deliverable == "Deliverable 1":
    st.title("Deliverable 1: Scenario Modeling")

    st.markdown("""
    Monte Carlo simulation engine (200 paths × 4 scenarios × 12 months)  
    AI-powered scenario interpretation via Claude API  
    Fan charts, uncertainty bands, resilience analysis
    """)

    # Example: generate sample scenario data
    scenario_df = data_generator.generate_scenarios(n_paths=200, n_months=12, n_scenarios=4)
    st.line_chart(scenario_df)

    # Example Plotly fan chart
    fig = plotting.fan_chart(scenario_df)
    st.plotly_chart(fig, use_container_width=True)

# -----------------------
# Deliverable 2: Insight Extraction
# -----------------------
elif deliverable == "Deliverable 2":
    st.title("Deliverable 2: Insight Extraction")

    st.markdown("""
    Analysis types: trends, anomalies, correlations, facility comparison, risk, executive summary  
    Structured prompt engineering for consistent AI output  
    Heatmaps, radar charts, anomaly timelines
    """)

    # Heatmap example
    heatmap_data = processing.generate_heatmap_data()
    fig = px.imshow(heatmap_data, text_auto=True, aspect="auto", color_continuous_scale="Viridis")
    st.plotly_chart(fig, use_container_width=True)

    # Radar chart example
    radar_data = processing.generate_radar_data()
    fig = px.line_polar(radar_data, r='value', theta='metric', line_close=True)
    st.plotly_chart(fig, use_container_width=True)

# -----------------------
# Deliverable 3: Strategic Dashboard
# -----------------------
elif deliverable == "Deliverable 3":
    st.title("Deliverable 3: Strategic Dashboard")

    st.markdown("""
    Full Plotly dashboard with tabbed interface, KPI cards, filtering  
    On-demand Claude API insights panel
    """)

    # KPI cards
    kpi_values = processing.generate_kpis()
    col1, col2, col3 = st.columns(3)
    col1.metric("Revenue", f"${kpi_values['revenue']:,}")
    col2.metric("Cost", f"${kpi_values['cost']:,}")
    col3.metric("Risk Score", f"{kpi_values['risk_score']:.2f}")

    # Interactive dashboard component
    df_dashboard = data_generator.generate_dashboard_data()
    fig = px.bar(df_dashboard, x="facility", y="value", color="scenario")
    st.plotly_chart(fig, use_container_width=True)

    # Claude API insights
    if st.button("Get AI Insights"):
        insights = llm_client.get_insights(df_dashboard)
        st.write(insights)

# -----------------------
# Deliverable 4: Documentation
# -----------------------
elif deliverable == "Deliverable 4":
    st.title("Deliverable 4: Documentation")

    st.markdown("""
    System & AI architecture docs  
    Quick start guide  
    Interview presentation guide  
    Extension/training guide
    """)

    # Display markdown documentation
    doc_path = "04_documentation/guides/presenting_this_project.md"
    try:
        with open(doc_path, "r", encoding="utf-8") as f:
            md_content = f.read()
        st.markdown(md_content)
    except FileNotFoundError:
        st.warning(f"Documentation file not found at {doc_path}")

# -----------------------
# Footer
# -----------------------
st.markdown("---")
st.markdown("LLM Scenario Modelling — Streamlit Version")
