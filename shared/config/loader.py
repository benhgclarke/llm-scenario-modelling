"""Project configuration loader — YAML settings + environment variables."""

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_PATH = Path(__file__).parent / "settings.yaml"


def load_settings() -> dict:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def get_anthropic_config() -> dict:
    return {
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
        "model": os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929"),
        "max_tokens": int(os.getenv("MAX_TOKENS", "4096")),
    }


SETTINGS = load_settings()
