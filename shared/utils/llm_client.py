"""Claude API client — shared across all deliverables."""

from anthropic import Anthropic

from shared.config.loader import get_anthropic_config

SYSTEM_PROMPT = """You are an expert operational data analyst specializing in manufacturing
and supply chain metrics. You provide clear, actionable insights based on data.

When analyzing data:
- Identify the most significant patterns and trends
- Highlight anomalies that warrant attention
- Quantify impacts where possible (use specific numbers from the data)
- Recommend concrete actions with expected outcomes
- Compare facilities and suggest best practice sharing
- Consider seasonality and external factors

Format responses with clear sections and bullet points for readability."""


def get_client() -> tuple[Anthropic, dict]:
    config = get_anthropic_config()
    if not config["api_key"]:
        raise ValueError(
            "ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key."
        )
    client = Anthropic(api_key=config["api_key"])
    return client, config


def query_claude(prompt: str, context: str = "", system: str = SYSTEM_PROMPT) -> str:
    """Send a prompt to Claude with optional data context. Returns response text."""
    client, config = get_client()

    user_message = prompt
    if context:
        user_message = f"DATA CONTEXT:\n{context}\n\nANALYSIS TASK:\n{prompt}"

    response = client.messages.create(
        model=config["model"],
        max_tokens=config["max_tokens"],
        system=system,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text
