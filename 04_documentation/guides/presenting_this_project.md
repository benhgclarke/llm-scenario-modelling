# Presenting This Project in an Interview

## Recommended Walkthrough Order

### 1. Start with the Big Picture (2 min)
- Open `notebooks/00_project_overview.ipynb`
- Show the project structure and explain the 4 deliverables
- Mention the tech stack: Python, Plotly, Claude API, Monte Carlo simulation

### 2. Show Deliverable 1: Scenario Modeling (5 min)
- Open `01_scenario_modeling/notebooks/01_scenario_modeling_walkthrough.ipynb`
- Key things to highlight:
  - The data generation approach (realistic patterns, seasonality, anomalies)
  - Monte Carlo simulation methodology
  - Fan charts showing uncertainty bands
  - How AI interprets the quantitative results

### 3. Show Deliverable 2: Insight Extraction (3 min)
- Open `02_insight_extraction/notebooks/02_insight_extraction_walkthrough.ipynb`
- Key things to highlight:
  - The prompt engineering approach (structured questions, CSV context)
  - 6 different analysis types from the same data
  - How statistical analysis feeds into AI interpretation
  - Correlation heatmaps and facility radar charts

### 4. Demo the Dashboard (3 min)
- Run `python main.py dashboard` beforehand
- Show filtering and tab navigation
- If API key is set, click "Generate Insights" live
- If not, show the notebook preview in Deliverable 3

### 5. Discuss Architecture (2 min)
- Reference `04_documentation/architecture/system_architecture.md`
- Explain the separation of concerns: shared utilities, independent deliverables
- Discuss how AI fits into the pipeline (not replacing analysis, augmenting it)

## Talking Points for Interviewers

### "Why this architecture?"
- Each deliverable is self-contained with its own notebook, code, data, and outputs
- Shared utilities prevent duplication
- Notebooks serve as living documentation that actually runs

### "How does the AI add value?"
- Statistical processing identifies patterns; AI explains what they mean in business terms
- Monte Carlo gives numbers; AI translates them into strategic recommendations
- The system works without AI (all charts, stats, scenarios) — AI is an enhancement layer

### "What would you do next?"
- Connect to live data sources (databases, APIs)
- Add alerting — automated anomaly notifications
- Build a feedback loop where AI recommendations are tracked against outcomes
- Add more sophisticated modeling (ARIMA, Prophet for time series)

### "How did you handle prompt engineering?"
- Structured numbered prompts for consistent output
- CSV data as context to keep AI grounded in real numbers
- Role-specific system prompts for different analysis types
- Graceful degradation when API key isn't available
