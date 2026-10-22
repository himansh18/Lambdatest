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
(tool: Claude, 2026-10-22)


ROLE
You are a senior SDET writing automatable regression tests for a web app.

CONTEXT
App under test: https://www.saucedemo.com (stand-in for a test management platform login).
Login form fields: Username, Password, Login button. There is NO email field, forgot-password link, Remember me checkbox, CAPTCHA, or visible session timeout.
Known users: standard_user, locked_out_user, problem_user. Password for all: secret_sauce.
Logout is via the burger menu. Successful login lands on /inventory.html.

TASK
Generate test cases for these five areas: valid login, invalid credentials, forgot password, session expiry, brute-force lockout.

OUTPUT FORMAT
- Gherkin only. One Feature per area (5 Features total). No commentary before or after.
- Every Scenario starts with a tag line: @id-LG-01 (prefix LG, IC, FP, SE, BF), a priority (@P1, @P2, @P3), a type (@positive, @negative, @boundary, @security), and @automatable or @design-only.
- Max 6 steps per scenario. Use concrete test data (real usernames, exact strings), never "valid credentials".
- Each Then step must be one deterministic, assertable outcome. No "or", no "per spec".

RULES
- 5 to 7 scenarios per area, no more. No duplicates (test account enumeration only once).
- Cover positive, negative and boundary cases (empty fields, whitespace, very long input, case-sensitivity, SQL/XSS strings).
- Do not invent UI elements or error texts. If an area cannot be tested on this app (forgot password, brute-force lockout), write the scenarios as @design-only and add a one-line comment "# Not present on SauceDemo: <reason>". Where a realistic proxy exists (e.g. session expiry by clearing cookies, locked_out_user for lockout), write an @automatable scenario using it.
- No scenarios that need email delivery, waits over 10 seconds, or server-side logs.

EXAMPLE OF EXPECTED STYLE
@id-LG-01 @P1 @positive @automatable
Scenario: Standard user logs in successfully
  Given I am on the login page
  When I log in as "standard_user" with password "secret_sauce"
  Then I am redirected to "/inventory.html"

SELF-CHECK
After the Gherkin, add a short comment block "# COVERAGE CHECK" listing, per area, the number of scenarios and any requirement you could not cover and why.


#### v2 result
Output: generated_tests/login.feature

What changed from v1 and what still needed work:
- Added role, context, strict Gherkin format, tags, limits and one example, so output became automatable and the right size.
- Told the model SauceDemo has no forgot-password or lockout, so it used @design-only tags and proxies (locked_out_user, cookie deletion) instead of inventing features.
- Still to verify: error messages and cookie name were supplied by the model and must be checked on the live site.
- Minor inconsistency: BF-04 is @automatable but carries a "not present" comment.