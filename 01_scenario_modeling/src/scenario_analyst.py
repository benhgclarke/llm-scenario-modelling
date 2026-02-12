"""AI-powered scenario analysis — uses Claude to interpret modeling results."""

from shared.utils.llm_client import query_claude


def analyze_scenario_results(scenario_summary_csv: str) -> str:
    """Comprehensive AI analysis of scenario projections."""
    return query_claude(
        prompt=(
            "Analyze these scenario projections for operational metrics. For each facility:\n"
            "1. Which metrics show the widest uncertainty bands (highest risk)?\n"
            "2. Where is the gap between optimistic and pessimistic scenarios largest?\n"
            "3. Which facility is most resilient under pessimistic conditions?\n"
            "4. What contingency plans should be prepared for worst-case scenarios?\n"
            "5. Where should management invest to narrow the uncertainty?\n"
            "6. Rank the top 5 strategic priorities based on scenario outcomes."
        ),
        context=scenario_summary_csv,
    )


def compare_scenario_paths(flat_scenarios_csv: str, metric: str, facility: str) -> str:
    """Deep-dive analysis of scenario paths for a specific metric/facility."""
    return query_claude(
        prompt=(
            f"Analyze the scenario projection paths for {metric} at {facility}.\n"
            "1. At what month do the scenarios begin to diverge significantly?\n"
            "2. What is the expected value and range at 3, 6, and 12 months?\n"
            "3. What early warning indicators should management watch?\n"
            "4. What actions could shift outcomes from pessimistic toward baseline?"
        ),
        context=flat_scenarios_csv,
    )


def generate_scenario_narrative(summary_csv: str) -> str:
    """Generate a board-ready narrative summary of scenario modeling results."""
    return query_claude(
        prompt=(
            "Write a 2-page executive briefing on these scenario projections. "
            "Structure it as:\n"
            "1. SITUATION: Current state of operations across facilities\n"
            "2. SCENARIOS: Key findings from optimistic through worst-case modeling\n"
            "3. RISKS: Top 3 risks with likelihood and impact\n"
            "4. OPPORTUNITIES: Where upside potential is greatest\n"
            "5. RECOMMENDATIONS: 5 prioritized actions with expected ROI\n\n"
            "Use confident, executive-level language. Be specific with numbers."
        ),
        context=summary_csv,
    )
