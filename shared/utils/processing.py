"""Shared data processing functions used across deliverables."""

import numpy as np
import pandas as pd


def compute_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Summary statistics per facility and metric."""
    summary = (
        df.groupby(["facility", "metric", "unit"])["value"]
        .agg(["mean", "std", "min", "max", "count"])
        .reset_index()
    )
    summary.columns = ["facility", "metric", "unit", "mean", "std", "min", "max", "count"]
    for col in ["mean", "std", "min", "max"]:
        summary[col] = summary[col].round(2)
    return summary


def compute_monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """Month-over-month change for each facility/metric."""
    df = df.sort_values(["facility", "metric", "date"]).copy()
    df["prev_value"] = df.groupby(["facility", "metric"])["value"].shift(1)
    df["mom_change"] = ((df["value"] - df["prev_value"]) / df["prev_value"] * 100).round(2)
    df["mom_abs_change"] = (df["value"] - df["prev_value"]).round(2)
    return df.dropna(subset=["mom_change"])


def detect_anomalies(df: pd.DataFrame, z_threshold: float = 2.0) -> pd.DataFrame:
    """Flag data points that deviate significantly from their group mean."""
    stats = df.groupby(["facility", "metric"])["value"].agg(["mean", "std"]).reset_index()
    stats.columns = ["facility", "metric", "group_mean", "group_std"]
    merged = df.merge(stats, on=["facility", "metric"])
    merged["z_score"] = (
        (merged["value"] - merged["group_mean"]) / merged["group_std"]
    ).round(2)
    anomalies = merged[merged["z_score"].abs() > z_threshold].copy()
    return anomalies[["date", "facility", "metric", "value", "unit", "z_score"]]


def compute_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-metric correlations per facility."""
    results = []
    for facility in df["facility"].unique():
        pivot = (
            df[df["facility"] == facility]
            .pivot_table(index="date", columns="metric", values="value")
        )
        corr = pivot.corr()
        for i, m1 in enumerate(corr.columns):
            for j, m2 in enumerate(corr.columns):
                if i < j:
                    results.append({
                        "facility": facility,
                        "metric_1": m1,
                        "metric_2": m2,
                        "correlation": round(corr.loc[m1, m2], 3),
                    })
    return pd.DataFrame(results)


def run_full_processing(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Run the complete processing pipeline and return all result DataFrames."""
    return {
        "raw": df,
        "summary": compute_summary_stats(df),
        "trends": compute_monthly_trends(df),
        "anomalies": detect_anomalies(df),
        "correlations": compute_correlations(df),
    }


def generate_heatmap_data() -> np.ndarray:
    """Generate sample heatmap data for visualization."""
    facilities = ["Plant Alpha", "Plant Beta", "Plant Gamma"]
    metrics = ["Production", "Quality", "Efficiency", "Cost"]
    rng = np.random.default_rng(42)
    return rng.integers(70, 100, size=(len(facilities), len(metrics)))


def generate_radar_data() -> pd.DataFrame:
    """Generate sample radar chart data."""
    metrics = ["Production", "Quality", "Efficiency", "Cost Control", "Safety"]
    values = [85, 90, 78, 88, 95]
    return pd.DataFrame({"metric": metrics, "value": values})


def generate_kpis() -> dict[str, int | float]:
    """Generate sample KPI values."""
    rng = np.random.default_rng(42)
    return {
        "revenue": rng.integers(500000, 1000000),
        "cost": rng.integers(300000, 500000),
        "risk_score": round(rng.uniform(2.0, 8.0), 2),
    }
