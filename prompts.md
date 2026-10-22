# Prompts Log

All prompts are pasted exactly as I wrote them, with no edits after the fact.

## Login Module

### Prompt v1
(tool used: Claude / 22-10-2026)

Generate test cases for the login page of a web app. Cover valid login, invalid credentials, forgot password, session expiry and brute-force lockout.

#### v1 result
Raw output: generated_tests/raw/login_v1_output.md
What was wrong:
- Markdown tables with free-text steps, not Gherkin or JSON, so not directly automatable.
- Many expected results were hedged ("per spec", "or a validation message").
- No concrete test data, and no priority or tags.
- Included features SauceDemo doesn't have (email login, forgot password, remember me, CAPTCHA).

### Prompt v2
(added later)