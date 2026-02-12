# Quick Start Guide

## Prerequisites

- Python 3.10 or later
- An Anthropic API key (for AI features — everything else works without it)

## Installation

```bash
# Clone / navigate to the project
cd "LLM Project"

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -e ".[dev]"

# Set up your API key (optional — for AI features)
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Running the Project

### Option 1: Full Pipeline via CLI

```bash
# Generate data → process → run scenarios (no API key needed)
python main.py all

# Include AI-generated insights (requires API key)
python main.py all --with-ai

# Launch the interactive dashboard
python main.py dashboard
# Open http://localhost:8050
```

### Option 2: Individual Steps

```bash
python main.py generate    # Generate synthetic data
python main.py process     # Run processing pipeline
python main.py scenarios   # Run Monte Carlo scenarios
python main.py insights    # Generate AI insights (needs API key)
python main.py dashboard   # Launch dashboard
```

### Option 3: Jupyter Notebooks (Recommended for Demos)

```bash
jupyter notebook

# Then open these in order:
# 1. 01_scenario_modeling/notebooks/01_scenario_modeling_walkthrough.ipynb
# 2. 02_insight_extraction/notebooks/02_insight_extraction_walkthrough.ipynb
# 3. 03_strategic_dashboard/notebooks/03_dashboard_walkthrough.ipynb
# 4. notebooks/00_project_overview.ipynb  (master overview)
```

## What You'll See

1. **Data Generation**: 24 months of operational KPIs across 3 manufacturing plants
2. **Processing**: Statistical summaries, trends, anomaly detection, cross-metric correlations
3. **Scenarios**: Monte Carlo projections under 4 conditions with uncertainty bands
4. **AI Insights**: Claude-powered trend analysis, risk assessment, executive summaries
5. **Dashboard**: Interactive charts with filtering and on-demand AI analysis
