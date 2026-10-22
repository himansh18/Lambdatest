# AI Usage Log

| Date | Tool | Task | What I used it for | What it produced | What I changed |
|---|---|---|---|---|---|
| 2026-10-22 | Claude | Task 1 | Planning the assessment, reviewing repo structure, debugging pytest/Playwright setup errors | Step-by-step plan, folder layout, run commands | Adapted the structure to my project, fixed the missing-folder error myself |

| 2026-10-22 | Claude | Task 2 (Login) | Ran naive prompt v1 to generate login test cases | ~65 test cases in markdown table | Saved raw output unedited; noted gaps in prompts.md (format, length, hedged results, features SauceDemo lacks) |

| 2026-10-22 | Claude | Task 2 (Login) | Diagnosed v1 output problems and drafted the v2 prompt; ran v2 in a fresh chat to generate Gherkin | Prompt v2 text from Claude; login Gherkin with 5 features, about 32 scenarios, tags and a coverage check | Used v2 unchanged. Saved output unedited as generated_tests/login.feature. Still need to verify error messages and cookie name on the live site |


| 2026-10-22 | ChatGPT | Task 2 (Login) — Automation | Wrote Python Playwright + pytest automation tests for five login scenarios using the manually verified SauceDemo behavior: empty fields, empty password, incorrect password, locked-out user, and successful login | Automated tests saved in `tests/ui/test_login.py`; executed `python -m pytest tests/ui/test_login.py -v` | All 5 login tests passed. Exact error messages and successful redirection to `/inventory.html` were verified. Dashboard and REST API automation tests are still pending. |

| 2026-10-22 | ChatGPT | Task 2 (Dashboard) — Automation | Generated Python Playwright + pytest UI tests for the SauceDemo inventory/dashboard module, covering product visibility, product count, price sorting, cart badge updates, and cart navigation | `tests/ui/test_dashboard.py` containing 5 automated UI tests | Ran the tests in headed mode with slow motion to observe browser behavior. Update this entry with the final pytest pass/fail results after confirming the terminal output. |