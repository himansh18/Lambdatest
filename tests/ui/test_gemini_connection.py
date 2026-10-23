
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

project_root = Path(__file__).resolve().parents[2]
load_dotenv(project_root / ".env.example")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY was not loaded.")

client = genai.Client(api_key=api_key)

print("Sending a real request to Gemini...")

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Reply with exactly: Gemini connection successful",
)

print("Gemini response:", response.text)
