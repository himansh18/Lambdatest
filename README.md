# TestMu AI SDET-1 Assessment: AI-Native Quality Engineering

An automated test suite (Python, Playwright, pytest) with an LLM wired into the framework. When a test fails, the failure details are sent to the Gemini API and a plain-English explanation with a suggested fix is saved to the report.

**Targets used as stand-ins** (the real TestMu platform isn't publicly accessible):
- UI (Login, Dashboard): https://www.saucedemo.com
- REST API: https://jsonplaceholder.typicode.com

## Setup

```powershell
git clone https://github.com/himansh18/testmu-sdet1-himanshusaraswat.git
cd testmu-sdet1-himanshusaraswat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install
copy .env.example .env
```

Open `.env` and set `GEMINI_API_KEY` to your own key. `.env` is git-ignored and must never be committed.

## How to run

```powershell
python -m pytest -v                    # whole suite
python -m pytest tests/ui -v           # UI tests (Login, Dashboard)
python -m pytest tests/api -v          # REST API tests
python scripts\check_gemini_connection.py   # optional: check the Gemini connection
```

## Where things live

| Item | Location |
|---|---|
| Raw prompts (v1 and v2 per module) | `prompts.md` |
| Generated test cases (Gherkin) | `generated_tests/` |
| Failure Explainer code | `ai/failure_explainer.py`, `ai/prompt_templates.py`, `conftest.py` |
| Sample LLM output | `reports/sample_output/failure_explanations.txt` |
| AI tools used | `ai-usage-log.md` |

## Design decisions

- **Python + Playwright:** Playwright has built-in auto-waiting, which reduces flaky tests, and Python makes it easy to combine browser tests, API tests (`requests`) and the Gemini SDK in one pytest framework.
- **Option A (Failure Explainer) over Option B:** it gives value at the moment of debugging and works from a single run, while a flaky-test classifier needs history across many runs.
- **Secrets:** the API key is loaded from an ignored `.env`, and failure text is redacted for keys, tokens and passwords before being sent to the LLM.
- **Stand-in targets:** SauceDemo has no forgot-password, session timeout or lockout counter, so those scenarios are marked `@design-only` in the generated Gherkin and proxies (locked user, cookie deletion) are used where possible.

## What I'd build next

- **Self-healing locators:** when a test fails on a missing selector, send the DOM to the LLM, get a suggested replacement selector, retry once, and report whether the healed test passed.
- **Flaky test classifier (Option B):** store each failure in a run history file and have the LLM classify failures as real bug, environment issue or flaky test, using results across many runs.
- **CI with GitHub Actions:** run the suite on every push and publish the failure explanations as a build artifact.
- **Prompt evaluation harness:** automatically score generated test cases (valid Gherkin, no duplicates, assertable outcomes) so prompt versions can be compared with numbers.
- **Opt-in LLM sharing:** make sending failure data to the LLM configurable, with stricter redaction of user data.