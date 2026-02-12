# System Architecture

## Overview

The AI-Enhanced Scenario Modeling system processes operational manufacturing data through a multi-stage pipeline, combining statistical analysis with LLM-powered interpretation.

## Data Flow

```
Raw Operational Data
    │
    ▼
┌────────────────────────┐
│  Data Processing Layer │
│  - Summary statistics  │
│  - Trend computation   │
│  - Anomaly detection   │
│  - Correlation matrix  │
└──────────┬─────────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
┌──────────┐ ┌──────────────┐
│ Scenario │ │   Insight    │
│ Modeling │ │  Extraction  │
│ Engine   │ │  Framework   │
│ (Monte   │ │ (Claude API) │
│  Carlo)  │ │              │
└────┬─────┘ └──────┬───────┘
     │               │
     └───────┬───────┘
             ▼
    ┌────────────────┐
    │   Dashboard    │
    │  (Plotly Dash) │
    │  - KPI cards   │
    │  - Charts      │
    │  - AI panel    │
    └────────────────┘
```

## Component Details

### Shared Layer (`shared/`)
- **config/**: YAML settings, environment loader
- **utils/llm_client.py**: Claude API wrapper with prompt templates
- **utils/processing.py**: Statistical processing functions
- **utils/plotting.py**: Consistent Plotly chart styling
- **data_generation/**: Synthetic data generator with realistic patterns

### Deliverable 1: Scenario Modeling (`01_scenario_modeling/`)
- Monte Carlo simulation engine (200 paths per scenario)
- 4 scenarios: optimistic (+15%), baseline, pessimistic (-15%), worst case (-30%)
- Projection horizons: 3, 6, 12 months
- AI interpretation via Claude for strategic narrative

### Deliverable 2: Insight Extraction (`02_insight_extraction/`)
- 6 analysis types: trends, anomalies, correlations, facility comparison, risk, executive summary
- Structured prompt engineering for consistent output
- Severity-tagged insights with metadata

### Deliverable 3: Dashboard (`03_strategic_dashboard/`)
- Plotly Dash with Bootstrap (Flatly theme)
- Real-time filtering: facility, metric, time range
- Tabbed interface: Trends, Scenarios, Anomalies, Correlations, AI Insights
- On-demand Claude API calls for AI analysis

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.10+ | Core runtime |
| Data | pandas, numpy | Processing and analysis |
| AI/LLM | Anthropic Claude API | Insight generation |
| Visualization | Plotly, Plotly Dash | Charts and dashboard |
| UI | Dash Bootstrap Components | Dashboard styling |
| Config | PyYAML, python-dotenv | Settings management |
| Notebooks | Jupyter | Walkthrough documentation |

## Configuration

All settings in `shared/config/settings.yaml`:
- Data categories and sample generation parameters
- Scenario variations and simulation count
- Insight focus areas
- Dashboard defaults

API key and model selection via `.env` file.
