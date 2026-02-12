"""
AI-Enhanced Data Analytics & Scenario Modeling
===============================================
CLI entry point — generate data, run processing, model scenarios,
extract AI insights, and launch the interactive dashboard.

Usage:
    python main.py generate     Generate synthetic operational metrics
    python main.py process      Run data processing pipeline
    python main.py scenarios    Run Monte Carlo scenario modeling
    python main.py insights     Generate AI insights (needs API key)
    python main.py dashboard    Launch Plotly Dash dashboard
    python main.py all          Run full pipeline
"""

import argparse
import importlib.util
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

# Ensure project root is importable
sys.path.insert(0, str(PROJECT_ROOT))


def _import(module_path: str, name: str):
    """Import a module by file path (handles digit-prefixed folders)."""
    spec = importlib.util.spec_from_file_location(name, str(PROJECT_ROOT / module_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── Commands ──────────────────────────────────────────────────────────────

def cmd_generate(_args):
    """Generate synthetic operational metrics data."""
    gen = _import("shared/data_generation/generate.py", "generate")
    df = gen.generate_operational_metrics()

    for folder in ["01_scenario_modeling", "02_insight_extraction", "03_strategic_dashboard"]:
        gen.save_data(df, str(PROJECT_ROOT / folder / "data"))

    print(f"Generated {len(df)} rows — {df['facility'].nunique()} facilities × {df['metric'].nunique()} metrics")
    print("Data saved to all deliverable folders.")


def cmd_process(_args):
    """Run the data processing pipeline."""
    gen = _import("shared/data_generation/generate.py", "generate")
    proc = _import("shared/utils/processing.py", "processing")

    df = gen.generate_operational_metrics()
    results = proc.run_full_processing(df)

    print("Processing pipeline results:")
    for name, result_df in results.items():
        print(f"  {name:15s} → {result_df.shape[0]:>5} rows × {result_df.shape[1]} cols")


def cmd_scenarios(_args):
    """Run Monte Carlo scenario modeling."""
    gen = _import("shared/data_generation/generate.py", "generate")
    modeler = _import("01_scenario_modeling/src/modeler.py", "modeler")

    raw = gen.generate_operational_metrics()
    results = modeler.run_all_scenarios(raw)
    summary = modeler.scenarios_endpoint_summary(results)

    print(f"Scenarios generated: {len(summary)} endpoint projections")
    print(f"\nSummary by scenario:")
    print(summary.groupby("scenario")[["projected_median", "uncertainty_range"]].mean().round(2))


def cmd_insights(_args):
    """Generate AI-powered insights (requires ANTHROPIC_API_KEY)."""
    gen = _import("shared/data_generation/generate.py", "generate")
    proc = _import("shared/utils/processing.py", "processing")
    extractor = _import("02_insight_extraction/src/extractor.py", "extractor")

    raw = gen.generate_operational_metrics()
    processed = proc.run_full_processing(raw)
    insights = extractor.extract_all_insights(processed)

    for category, text in insights.items():
        print(f"\n{'=' * 70}")
        print(f"  {category.upper().replace('_', ' ')}")
        print(f"{'=' * 70}")
        print(text)


def cmd_dashboard(_args):
    """Launch the interactive Plotly Dash dashboard."""
    app_mod = _import("03_strategic_dashboard/src/app.py", "dashboard_app")
    app_mod.run_dashboard()


def cmd_all(args):
    """Run the full pipeline end-to-end."""
    print("=" * 60)
    print("  AI-Enhanced Scenario Modeling — Full Pipeline")
    print("=" * 60)

    print("\n[1/3] Generating data...")
    cmd_generate(args)

    print("\n[2/3] Processing data...")
    cmd_process(args)

    print("\n[3/3] Running scenarios...")
    cmd_scenarios(args)

    if getattr(args, "with_ai", False):
        print("\n[4/4] Generating AI insights...")
        cmd_insights(args)

    print("\n" + "=" * 60)
    print("  Pipeline complete!")
    print("  Run:  python main.py dashboard")
    print("  Open: http://localhost:8050")
    print("=" * 60)


# ── CLI ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="AI-Enhanced Data Analytics & Scenario Modeling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("generate", help="Generate synthetic operational metrics data")
    sub.add_parser("process", help="Run data processing pipeline")
    sub.add_parser("scenarios", help="Run Monte Carlo scenario modeling")
    sub.add_parser("insights", help="Generate AI insights (requires API key)")
    sub.add_parser("dashboard", help="Launch interactive dashboard")

    all_cmd = sub.add_parser("all", help="Run full pipeline")
    all_cmd.add_argument("--with-ai", action="store_true", help="Include AI insights (needs API key)")

    args = parser.parse_args()
    commands = {
        "generate": cmd_generate,
        "process": cmd_process,
        "scenarios": cmd_scenarios,
        "insights": cmd_insights,
        "dashboard": cmd_dashboard,
        "all": cmd_all,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
