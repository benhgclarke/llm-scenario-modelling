# AI-Enhanced Data Analytics & Scenario Modeling

An end-to-end AI-augmented analytics system for operational manufacturing data. Combines statistical analysis, Monte Carlo simulation, and Claude API-powered interpretation to deliver actionable strategic insights through Jupyter notebooks and an interactive dashboard.

## Quick Start

```bash
# 1. Install dependencies
pip install -e ".[dev]"

# 2. Set up API key (optional — everything except AI insights works without it)
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 3. Run full pipeline
python main.py all

# 4. Launch dashboard
python main.py dashboard
# → http://localhost:8050

# 5. Or explore via notebooks
jupyter notebook
# → Start with notebooks/00_project_overview.ipynb
```

## Project Structure

```
├── notebooks/
│   └── 00_project_overview.ipynb           Master overview & walkthrough
│
├── 01_scenario_modeling/                   DELIVERABLE 1
│   ├── notebooks/                          Step-by-step walkthrough
│   ├── src/modeler.py                      Monte Carlo simulation engine
│   ├── src/scenario_analyst.py             AI-powered scenario interpretation
│   ├── data/                               Raw operational metrics
│   └── outputs/                            Charts, projections, CSVs
│
├── 02_insight_extraction/                  DELIVERABLE 2
│   ├── notebooks/                          Step-by-step walkthrough
│   ├── src/extractor.py                    6-type AI insight framework
│   ├── data/                               Raw operational metrics
│   └── outputs/                            Charts, analysis outputs
│
├── 03_strategic_dashboard/                 DELIVERABLE 3
│   ├── notebooks/                          Component preview & launch guide
│   ├── src/app.py                          Plotly Dash application
│   ├── data/                               Raw operational metrics
│   └── outputs/                            Chart exports
│
├── 04_documentation/                       DELIVERABLE 4
│   ├── architecture/                       System & AI architecture docs
│   ├── guides/                             Quick start, presentation guide
│   └── training/                           Extension & training materials
│
├── shared/                                 Shared infrastructure
│   ├── config/                             YAML settings + environment loader
│   ├── utils/                              LLM client, processing, plotting
│   └── data_generation/                    Synthetic data generator
│
├── main.py                                 CLI entry point
└── pyproject.toml                          Dependencies
```

## Deliverables

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Automated Scenario Modeling** | Monte Carlo simulation engine projecting 10 KPIs under 4 scenarios with AI interpretation |
| 2 | **Insight Extraction Framework** | 6 AI analysis types: trends, anomalies, correlations, facility comparison, risk, executive summary |
| 3 | **Strategic Dashboard** | Interactive Plotly Dash app with filtering, charts, and on-demand AI insights |
| 4 | **Documentation & Training** | Architecture docs, quick start guide, presentation guide, extension guide |

## CLI Commands

| Command | Description |
|---------|-------------|
| `python main.py generate` | Generate 24 months of synthetic operational data for 3 facilities |
| `python main.py process` | Run statistical processing: summaries, trends, anomaly detection, correlations |
| `python main.py scenarios` | Run Monte Carlo projections: optimistic, baseline, pessimistic, worst case |
| `python main.py insights` | Generate AI insights via Claude API (requires `ANTHROPIC_API_KEY`) |
| `python main.py dashboard` | Launch interactive dashboard at http://localhost:8050 |
| `python main.py all` | Run full pipeline (add `--with-ai` for Claude insights) |

## Key Features

- **10 operational metrics** across 3 manufacturing facilities over 24 months
- **Monte Carlo simulation** with 200 paths × 4 scenarios × 12-month horizon
- **Statistical pipeline**: summary stats, MoM trends, z-score anomaly detection, Pearson correlations
- **6 AI analysis types** via Claude API with structured prompt engineering
- **Interactive dashboard** with real-time filtering, KPI cards, fan charts, heatmaps, radar plots
- **Portfolio-ready notebooks** with step-by-step walkthroughs for each deliverable

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.13+ |
| Data | pandas, numpy, scipy |
| AI/LLM | Anthropic Claude API |
| Visualization | Plotly, Plotly Dash |
| Dashboard UI | Dash Bootstrap Components (Flatly) |
| Notebooks | Jupyter |
| Config | PyYAML, python-dotenv |
