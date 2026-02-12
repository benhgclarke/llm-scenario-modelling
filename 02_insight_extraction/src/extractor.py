"""AI-powered insight extraction framework.

Structured extraction of trends, anomalies, correlations, comparisons,
risk assessments, and executive summaries using Claude API.
"""

from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd

from shared.utils.llm_client import query_claude


@dataclass
class Insight:
    """A single extracted insight with metadata."""
    category: str          # trend, anomaly, correlation, comparison, risk, executive
    title: str
    content: str
    severity: str          # info, warning, critical
    facility: str | None = None
    metric: str | None = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# ── Individual analysis functions ──────────────────────────────────────────

def analyze_trends(trends_csv: str) -> str:
    return query_claude(
        prompt=(
            "Analyze these operational metric trends across facilities.\n"
            "1. What are the most significant improvements over the period?\n"
            "2. Which metrics are deteriorating and need attention?\n"
            "3. Are there seasonal patterns visible?\n"
            "4. Which facility shows the strongest overall trajectory?\n"
            "5. What actions should be taken based on these trends?"
        ),
        context=trends_csv,
    )


def analyze_anomalies(anomalies_csv: str) -> str:
    return query_claude(
        prompt=(
            "These data points were flagged as statistical anomalies (z-score > 2.0).\n"
            "1. Which anomalies represent real operational issues vs normal variation?\n"
            "2. Are there clusters of anomalies that suggest systemic problems?\n"
            "3. Prioritize by business impact (high/medium/low)\n"
            "4. Recommend investigation steps for the top 3 anomalies\n"
            "5. What monitoring thresholds would catch these earlier?"
        ),
        context=anomalies_csv,
    )


def analyze_correlations(correlations_csv: str) -> str:
    return query_claude(
        prompt=(
            "Analyze these cross-metric correlations for operational insights.\n"
            "1. Which correlations reveal likely causal relationships?\n"
            "2. Which are spurious or coincidental?\n"
            "3. What operational levers could management pull based on these?\n"
            "4. Are there unexpected correlations that warrant investigation?\n"
            "5. How do correlation patterns differ across facilities?"
        ),
        context=correlations_csv,
    )


def compare_facilities(summary_csv: str) -> str:
    return query_claude(
        prompt=(
            "Compare operational performance across these facilities.\n"
            "1. Rank facilities by overall operational excellence\n"
            "2. Which facility is best-in-class for each metric?\n"
            "3. Where are the largest performance gaps between best and worst?\n"
            "4. What specific practices should transfer from top to bottom performers?\n"
            "5. Which facility has the most improvement potential?"
        ),
        context=summary_csv,
    )


def assess_risks(anomalies_csv: str, trends_csv: str) -> str:
    context = f"ANOMALIES:\n{anomalies_csv}\n\nTRENDS:\n{trends_csv}"
    return query_claude(
        prompt=(
            "Generate an operational risk assessment.\n"
            "1. Top 5 operational risks ranked by likelihood and impact\n"
            "2. Leading indicators that could predict deterioration\n"
            "3. Risk mitigation strategies for each identified risk\n"
            "4. Metrics that serve as early warning signals\n"
            "5. Recommended monitoring thresholds and alert triggers"
        ),
        context=context,
    )


def generate_executive_summary(summary_csv: str, trends_csv: str, anomalies_csv: str) -> str:
    context = (
        f"SUMMARY STATISTICS:\n{summary_csv}\n\n"
        f"RECENT TRENDS:\n{trends_csv}\n\n"
        f"ANOMALIES DETECTED:\n{anomalies_csv}"
    )
    return query_claude(
        prompt=(
            "Generate an executive summary of operational performance:\n"
            "1. Overall health assessment (Red/Yellow/Green per facility)\n"
            "2. Top 3 wins and top 3 concerns\n"
            "3. Key metrics trending in the wrong direction\n"
            "4. Recommended immediate actions (next 30 days)\n"
            "5. Strategic recommendations (next quarter)"
        ),
        context=context,
    )


# ── Orchestration ─────────────────────────────────────────────────────────

def extract_all_insights(processed: dict[str, pd.DataFrame]) -> dict[str, str]:
    """Run all insight extraction analyses.

    Args:
        processed: Dict from run_full_processing() with keys:
                   'raw', 'summary', 'trends', 'anomalies', 'correlations'

    Returns:
        Dict mapping analysis type to Claude's response text.
    """
    insights = {}

    # Trends
    trends_csv = processed["trends"].tail(200).to_csv(index=False)
    insights["trends"] = analyze_trends(trends_csv)

    # Anomalies
    anomalies_csv = processed["anomalies"].to_csv(index=False)
    if len(processed["anomalies"]) > 0:
        insights["anomalies"] = analyze_anomalies(anomalies_csv)
    else:
        insights["anomalies"] = "No significant anomalies detected."

    # Correlations (strong only)
    corr = processed["correlations"]
    strong = corr[corr["correlation"].abs() > 0.5]
    if len(strong) > 0:
        insights["correlations"] = analyze_correlations(strong.to_csv(index=False))
    else:
        insights["correlations"] = "No strong cross-metric correlations found."

    # Facility comparison
    insights["facility_comparison"] = compare_facilities(
        processed["summary"].to_csv(index=False)
    )

    # Risk assessment
    insights["risk_assessment"] = assess_risks(anomalies_csv, trends_csv)

    # Executive summary
    insights["executive_summary"] = generate_executive_summary(
        summary_csv=processed["summary"].to_csv(index=False),
        trends_csv=trends_csv,
        anomalies_csv=anomalies_csv,
    )

    return insights
