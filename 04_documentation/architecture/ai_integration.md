# AI Integration Architecture

## Claude API Integration

### How LLMs Fit in the Pipeline

The system uses Claude at three levels:

1. **Data Interpretation** — Claude receives processed statistical data (CSV format) and provides natural-language analysis of trends, anomalies, and patterns.

2. **Scenario Analysis** — After Monte Carlo simulations generate projection bands, Claude interprets what the scenarios mean strategically and recommends actions.

3. **Executive Communication** — Claude generates board-ready summaries, risk assessments, and facility comparisons from quantitative inputs.

### Prompt Engineering Approach

Each analysis type uses a specialized prompt template:

```
SYSTEM PROMPT (shared):
  "You are an expert operational data analyst..."
  - Defines role and output expectations
  - Sets formatting standards

USER MESSAGE:
  "DATA CONTEXT:\n{csv_data}\n\nANALYSIS TASK:\n{specific_prompt}"
  - Data context: relevant CSV subset
  - Analysis task: numbered specific questions
```

Key prompt design decisions:
- **Numbered questions** force structured output that's easy to parse
- **Specific data references** ("use the numbers from the data") prevent hallucination
- **Role-specific framing** ("executive briefing", "risk assessment") controls tone
- **CSV context** keeps data grounded — Claude reads real numbers, not descriptions

### Analysis Types

| Type | Input Data | Prompt Focus | Output |
|------|-----------|-------------|--------|
| Trend Analysis | MoM change CSV | Improvements, deteriorations, seasonal patterns | Prioritized findings + actions |
| Anomaly Assessment | Z-score flagged points | Real issues vs. noise, business impact | Prioritized investigation steps |
| Correlation Analysis | Strong correlations (|r|>0.5) | Causal vs. spurious, operational levers | Actionable relationships |
| Facility Comparison | Summary stats | Rankings, best practices, gaps | Transfer recommendations |
| Risk Assessment | Anomalies + trends | Top risks, early warnings, mitigation | Risk register with priorities |
| Executive Summary | All processed data | Health assessment, wins/concerns, actions | Board-ready narrative |

### Error Handling

- All AI calls wrapped in try/except — dashboard and notebooks degrade gracefully without API key
- API key validation at client creation time with clear error message
- Model and token limits configurable via `.env`

### Cost Considerations

- Each full insight extraction run makes ~6 API calls
- Context is trimmed (e.g., `tail(200)` for trends) to control token usage
- Correlations filtered to strong (|r|>0.5) before sending to API
