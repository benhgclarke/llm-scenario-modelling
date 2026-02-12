"""Monte Carlo scenario modeling engine.

Projects operational metrics forward under optimistic, baseline,
pessimistic, and worst-case conditions using simulation.
"""

import numpy as np
import pandas as pd

from shared.config.loader import SETTINGS


def project_metric(
    historical: pd.Series,
    months_ahead: int,
    scenario_multiplier: float,
    num_simulations: int = 200,
) -> pd.DataFrame:
    """Project a single metric forward using Monte Carlo simulation.

    Args:
        historical: Time-ordered series of historical values.
        months_ahead: Number of months to project.
        scenario_multiplier: Scale factor for the trend component.
        num_simulations: Number of simulation paths.

    Returns:
        DataFrame with columns: month, p10, p25, median, p75, p90, mean, std
    """
    rng = np.random.default_rng(42)
    std = historical.std()

    # Estimate trend from most recent 6 months
    recent = historical.tail(6)
    trend = (recent.iloc[-1] - recent.iloc[0]) / max(len(recent) - 1, 1) if len(recent) > 1 else 0

    simulations = np.zeros((num_simulations, months_ahead))
    start = historical.iloc[-1]

    for sim in range(num_simulations):
        current = start
        for month in range(months_ahead):
            noise = rng.normal(0, std * 0.3)
            current = current + (trend * scenario_multiplier) + noise
            simulations[sim, month] = current

    return pd.DataFrame({
        "month": range(1, months_ahead + 1),
        "p10": np.percentile(simulations, 10, axis=0).round(2),
        "p25": np.percentile(simulations, 25, axis=0).round(2),
        "median": np.percentile(simulations, 50, axis=0).round(2),
        "p75": np.percentile(simulations, 75, axis=0).round(2),
        "p90": np.percentile(simulations, 90, axis=0).round(2),
        "mean": simulations.mean(axis=0).round(2),
        "std": simulations.std(axis=0).round(2),
    })


def run_all_scenarios(raw_df: pd.DataFrame) -> dict:
    """Run scenarios for every facility / metric / scenario combination.

    Returns:
        Nested dict: {facility: {metric: {scenario_name: projection_df}}}
    """
    cfg = SETTINGS["scenarios"]
    variations = cfg["variation"]
    num_sims = cfg["num_simulations"]
    max_horizon = max(cfg["time_horizons"])

    results = {}
    for facility in raw_df["facility"].unique():
        results[facility] = {}
        fac_df = raw_df[raw_df["facility"] == facility]

        for metric in raw_df["metric"].unique():
            series = (
                fac_df[fac_df["metric"] == metric]
                .sort_values("date")["value"]
                .reset_index(drop=True)
            )
            if len(series) < 3:
                continue

            results[facility][metric] = {}
            for scenario_name, multiplier in variations.items():
                results[facility][metric][scenario_name] = project_metric(
                    series, max_horizon, multiplier, num_sims
                )

    return results


def scenarios_to_flat_df(results: dict) -> pd.DataFrame:
    """Flatten the nested scenario results into a single DataFrame."""
    rows = []
    for facility, metrics in results.items():
        for metric, scenarios in metrics.items():
            for scenario_name, proj_df in scenarios.items():
                for _, row in proj_df.iterrows():
                    rows.append({
                        "facility": facility,
                        "metric": metric,
                        "scenario": scenario_name,
                        "month": int(row["month"]),
                        "p10": row["p10"],
                        "median": row["median"],
                        "p90": row["p90"],
                        "mean": row["mean"],
                    })
    return pd.DataFrame(rows)


def scenarios_endpoint_summary(results: dict) -> pd.DataFrame:
    """Summary of final-month projections across all scenarios."""
    rows = []
    for facility, metrics in results.items():
        for metric, scenarios in metrics.items():
            for scenario_name, proj_df in scenarios.items():
                final = proj_df.iloc[-1]
                rows.append({
                    "facility": facility,
                    "metric": metric,
                    "scenario": scenario_name,
                    "projected_median": final["median"],
                    "projected_p10": final["p10"],
                    "projected_p90": final["p90"],
                    "uncertainty_range": round(final["p90"] - final["p10"], 2),
                    "projection_months": len(proj_df),
                })
    return pd.DataFrame(rows)
