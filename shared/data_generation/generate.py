"""Synthetic operational metrics generator.

Creates realistic manufacturing KPI data with trends, seasonality,
facility-level variation, and occasional anomalies for 3 plants over 24 months.
"""

import numpy as np
import pandas as pd

from shared.config.loader import SETTINGS

# Metric profiles: (base_value, std_dev, unit, monthly_trend)
METRIC_PROFILES = {
    "production_output":      (1000, 80,   "units",   5.0),
    "quality_rate":           (96.5, 1.2,  "%",       0.05),
    "equipment_uptime":       (92.0, 3.0,  "%",       0.10),
    "labor_efficiency":       (85.0, 4.0,  "%",       0.15),
    "inventory_turnover":     (8.5,  0.8,  "turns",   0.02),
    "order_fulfillment_rate": (94.0, 2.5,  "%",       0.08),
    "cycle_time_hours":       (4.2,  0.5,  "hours",  -0.02),
    "defect_rate_ppm":        (1200, 150,  "ppm",    -8.0),
    "energy_cost_per_unit":   (2.30, 0.25, "$/unit",  0.01),
    "on_time_delivery_pct":   (91.0, 3.0,  "%",       0.10),
}

FACILITY_PROFILES = {
    "Plant Alpha": {"multiplier": 1.00, "volatility": 1.0},
    "Plant Beta":  {"multiplier": 0.92, "volatility": 1.2},   # underperformer, noisier
    "Plant Gamma": {"multiplier": 1.06, "volatility": 0.85},  # top performer, stable
}


def generate_operational_metrics() -> pd.DataFrame:
    """Generate full synthetic dataset."""
    cfg = SETTINGS["data"]["sample"]
    num_months = cfg["num_months"]
    facility_names = cfg["facility_names"]
    rng = np.random.default_rng(42)

    dates = pd.date_range(end=pd.Timestamp.now().normalize(), periods=num_months, freq="MS")
    rows = []

    for facility in facility_names:
        profile = FACILITY_PROFILES.get(facility, {"multiplier": 1.0, "volatility": 1.0})

        for metric_name, (base, std, unit, trend) in METRIC_PROFILES.items():
            for i, date in enumerate(dates):
                trend_adj = trend * i
                seasonal = np.sin(2 * np.pi * i / 12) * std * 0.3
                noise = rng.normal(0, std * profile["volatility"])

                # Inject occasional anomalies (~3% chance)
                if rng.random() < 0.03:
                    noise += rng.choice([-1, 1]) * std * 3

                value = (base + trend_adj + seasonal + noise) * profile["multiplier"]

                if unit == "%":
                    value = np.clip(value, 0, 100)
                elif unit != "$/unit":
                    value = max(0, value)

                rows.append({
                    "date": date,
                    "facility": facility,
                    "metric": metric_name,
                    "value": round(value, 2),
                    "unit": unit,
                })

    return pd.DataFrame(rows)


def save_data(df: pd.DataFrame, output_dir: str) -> str:
    """Save DataFrame to CSV in the given directory. Returns path."""
    from pathlib import Path
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "operational_metrics.csv"
    df.to_csv(path, index=False)
    return str(path)


if __name__ == "__main__":
    df = generate_operational_metrics()
    path = save_data(df, str(SETTINGS.get("_output", "shared/data_generation")))
    print(f"Generated {len(df)} rows → {path}")
