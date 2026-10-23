
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from ai.prompt_templates import FAILURE_EXPLAINER_PROMPT

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

SENSITIVE_VALUE_PATTERNS = (
    re.compile(
        r"(?i)\b(api[_-]?key|access[_-]?token|auth(?:orization)?|"
        r"password|secret)\b(\s*[:=]\s*|\s+)([^\s,;]+)"
    ),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]+=*"),
)


def redact_sensitive_text(text: str) -> str:
    """Redact common credential values before sending failure text externally."""
    redacted = SENSITIVE_VALUE_PATTERNS[0].sub(
        lambda match: f"{match.group(1)}{match.group(2)}[REDACTED]",
        text,
    )
    return SENSITIVE_VALUE_PATTERNS[1].sub("Bearer [REDACTED]", redacted)


def explain_failure(test_name: str, failure_details: str) -> str:
    """Use a real Gemini API request to explain a pytest failure."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "AI explanation unavailable: GEMINI_API_KEY was not loaded."

    prompt = FAILURE_EXPLAINER_PROMPT.format(
        test_name=test_name,
        failure_details=redact_sensitive_text(failure_details)[:6000],
    )

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )
        return response.text or "Gemini returned an empty response."
    except Exception as exc:
        # Preserve the original test result even if the AI service fails.
        return f"AI explanation unavailable: {type(exc).__name__}: {exc}"
