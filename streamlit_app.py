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
    st.title("Deliverable 3: Str
