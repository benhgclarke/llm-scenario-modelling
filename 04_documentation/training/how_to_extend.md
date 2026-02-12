# How to Extend This System

## Adding a New Metric

1. Add the metric definition to `shared/data_generation/generate.py`:
   ```python
   METRIC_PROFILES["new_metric_name"] = (base_value, std_dev, "unit", trend_per_month)
   ```

2. Add the metric name to `shared/config/settings.yaml` under `data.categories`

3. Regenerate data: `python main.py generate`

4. Everything else (processing, scenarios, dashboard) picks it up automatically.

## Adding a New Facility

1. Add to `FACILITY_PROFILES` in `shared/data_generation/generate.py`:
   ```python
   FACILITY_PROFILES["Plant Delta"] = {"multiplier": 0.95, "volatility": 1.1}
   ```

2. Add the name to `shared/config/settings.yaml` under `data.sample.facility_names`

3. Add a color to `shared/utils/plotting.py`:
   ```python
   COLORS["Plant Delta"] = "#AB63FA"
   ```

## Adding a New Analysis Type

1. Add a function to `02_insight_extraction/src/extractor.py`:
   ```python
   def analyze_new_thing(data_csv: str) -> str:
       return query_claude(
           prompt="Your analysis prompt here...",
           context=data_csv,
       )
   ```

2. Add to `extract_all_insights()` to include it in the standard pipeline

3. Add a section in the Deliverable 2 notebook to visualize and display it

## Adding a New Scenario Type

1. Add to `shared/config/settings.yaml` under `scenarios.variation`:
   ```yaml
   extreme_upside: 1.30  # +30% trend amplification
   ```

2. Add a color to `shared/utils/plotting.py`:
   ```python
   SCENARIO_COLORS["extreme_upside"] = "#19D3F3"
   ```

## Connecting Real Data

Replace the data generation step with a real data loader:

1. Create `shared/data_loaders/your_source.py`
2. Implement a function that returns a DataFrame with columns: `date, facility, metric, value, unit`
3. Use it instead of `generate_operational_metrics()` in the notebooks and dashboard
