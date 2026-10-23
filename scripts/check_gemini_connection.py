"""Optional live Gemini connectivity check; this is intentionally not a pytest test."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def main() -> int:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY is not set in .env.")
        return 1

    print("Sending a real request to Gemini...")
    try:
        response = genai.Client(api_key=api_key).models.generate_content(
            model="gemini-3.5-flash-lite",
            contents="Reply with exactly: Gemini connection successful",
        )
    except Exception as exc:
        print(f"Gemini connection failed: {type(exc).__name__}: {exc}")
        return 1

    print("Gemini response:", response.text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
