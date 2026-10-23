# Prompts Log

Prompts are documented in the order they were used. Original prompts should be preserved exactly as entered. Results, observations, and validation outcomes are documented separately from the prompt text.

## Login Module

### Prompt v1 — Initial Test Case Generation

**Tool:** Claude  
**Date:** 2026-10-22

**Prompt:**

Generate test cases for the login page of a web app. Cover valid login, invalid credentials, forgot password, session expiry and brute-force lockout.

#### v1 Result

**Raw output:** `generated_tests/raw/login_v1_output.md`

**Problems identified:**

- Markdown tables with free-text steps, not Gherkin or JSON, so not directly automatable.
- Many expected results were hedged ("per spec", "or a validation message").
- No concrete test data, and no priority or tags.
- Included features SauceDemo doesn't have (email login, forgot password, remember me, CAPTCHA).

**Conclusion:** The prompt did not provide enough application context or define a strict, automation-friendly output format. Prompt v2 was created to address these issues.

### Prompt v2 — Refined Gherkin Generation

**Tool:** Claude  
**Date:** 2026-10-22

**Prompt:**

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

#### v2 Result

**Output:** `generated_tests/login.feature`

**Improvements over v1:**

- Added role, context, strict Gherkin format, tags, limits, and an example.
- Clarified that unsupported SauceDemo features should not be invented.
- Required concrete test data, deterministic expected outcomes, and a coverage check.

**Remaining issues identified during review:**

- Error messages and the cookie name supplied by the generated output needed verification against the live application.
- BF-04 was tagged `@automatable` while also carrying a comment that the functionality was not present. This inconsistency needed review.

**Conclusion:** Prompt v2 improved the structure and relevance of the generated cases, but the output still needed manual verification.

### Prompt v3 — Login UI Automation

**Tool:** ChatGPT  
**Date:** 2026-10-22

**Prompt:**

ROLE
You are a Python SDET building automated UI regression tests using Playwright and pytest.

Task
TASK
Write Python Playwright tests for the login module using the existing pytest framework.

REQUIREMENTS

Cover empty login fields, empty password, incorrect password, locked-out user, and successful login.

Use pytest and Playwright's synchronous Python API.

Use clear, descriptive test names.

Assert exact error messages for negative login scenarios.

For successful login, assert the resulting URL and that the inventory list is visible.

Use stable locators and Playwright assertions.

Do not invent error messages or application behavior.

Do not overwrite unrelated files or duplicate existing tests.

Return the complete Python code for tests/ui/test_login.py.

VALIDATION
Run the tests using:
python -m pytest tests/ui/test_login.py -v

Record the actual pass/fail results separately. Do not claim tests passed unless execution confirms it.

#### v3 Result

**Output:** `tests/ui/test_login.py`

**Validation command:**

`python -m pytest tests/ui/test_login.py -v`

**Validation result:** All five Login tests passed, according to the terminal output recorded on 2026-10-22.

**What worked:**

- Implemented five Login scenarios using Python, Playwright, and pytest.
- Verified exact error messages for negative Login scenarios.
- Verified successful navigation to the inventory page.

**Conclusion:** The refined prompt produced executable Python UI tests, and all five tests passed in the reported run.

---

## Dashboard Module

### Prompt v1 — Dashboard UI Automation

**Tool:** ChatGPT  
**Date:** 2026-10-22

**Prompt:**

ROLE

You are a senior Python SDET writing reliable UI automation tests using Playwright and pytest.

CONTEXT

Project: Lambdatest
Application: https://www.saucedemo.com/
Language: Python only. Do not use JavaScript.
Existing login tests: `tests/ui/test_login.py`
New test file: `tests/ui/test_dashboard.py`

TASK

Inspect the existing project structure and the application's inventory page after login. Generate automated tests for the dashboard/inventory module based only on behavior and UI elements that can actually be verified.

REQUIREMENTS

- Use Python, pytest, and Playwright's synchronous API.
- Follow the existing project's conventions and fixtures.
- Do not modify or duplicate the existing login tests.
- Use descriptive test names, stable locators, and explicit assertions.
- Cover meaningful inventory-page functionality, using only features confirmed to exist.
- Do not invent UI elements, expected results, or application behavior.
- Keep tests independent and avoid unnecessary fixed sleeps.
- If a behavior cannot be verified, explain the limitation instead of inventing an assertion.
- Return the complete code for `tests/ui/test_dashboard.py` and list any assumptions.

VALIDATION

Run:

`python -m pytest tests/ui/test_dashboard.py -v`

Report the actual test results. Do not claim tests passed unless the command confirms it.

#### Dashboard v1 Result

**Output:** `tests/ui/test_dashboard.py`

**Tests generated:**

1. `test_inventory_page_displays_products` — checks that product names and prices are visible.
2. `test_inventory_displays_six_products` — checks that six products are displayed.
3. `test_inventory_can_be_sorted_by_price_low_to_high` — checks ascending price sorting.
4. `test_adding_product_updates_cart_badge` — checks the cart badge and Remove button after adding a product.
5. `test_shopping_cart_navigation_opens_cart_page` — checks navigation to the cart page and its heading.

**Review observations:**

- The tests use a fixture to log in before checking inventory functionality.
- The test cases use Playwright locators and assertions.
- The first test contains a somewhat redundant nonzero product-count assertion after checking that the first product is visible.
- The code was run in headed mode with slow motion so browser actions could be observed.

**Validation status:** The user reported that headed execution was working. The final pass/fail summary for all five Dashboard tests has not yet been recorded here; update this section from the actual terminal output.

**Conclusion:** The Dashboard tests cover core inventory and shopping-cart behavior. Their final status should be based on the pytest results, not solely on the visible browser execution.

---



## API Test Generation Prompt

**Module:** REST API testing

**Prompt:**

Act as a senior SDET and API test engineer. Generate comprehensive REST API test scenarios for a hypothetical resource-management API. Clearly state all assumptions and do not claim that the API exists or that any tests have executed.

Cover these modules:

1. **Authentication and token validation:** valid token, missing token, malformed token, expired token, and insufficient permissions.
2. **CRUD operations:** create a resource, retrieve an existing resource, update a resource, partially update a resource, delete a resource, and access a nonexistent resource.
3. **Error handling:** malformed JSON, missing required fields, invalid field values, unsupported HTTP methods, server errors, and consistent error-response formats.
4. **Rate limiting:** requests within the allowed limit, requests exceeding the limit, rate-limit response headers, and behavior after the limit resets.
5. **Schema validation:** required fields, data types, formats, unexpected fields, null values, and response-schema consistency.

For each scenario, provide a test ID, objective, HTTP method, assumed endpoint, preconditions, request data, expected HTTP status, and expected response behavior.

Use Gherkin format. Separate positive, negative, boundary, and security cases. Explicitly label assumed endpoints and expected statuses as examples requiring confirmation against the actual API contract. Do not fabricate execution results.

**Output requirements:** Produce a traceable API test-design document that can later be implemented in Python using pytest and requests once the actual API contract and environment are available.


**API module — prompt refinement and validation notes**

- **Initial attempt:** The nonexistent-resource test assumed that `GET /posts/999999` would return HTTP 200 with an empty JSON object.
- **Observed failure:** The public API returned HTTP 404, causing the assertion to fail.
- **Refinement:** Updated the expected status to 404 based on the observed response, instead of relying on an unverified assumption.
- **Validation:** The corrected test must be rerun before recording the final pass count. This finding applies to the tested public API endpoint and is not a universal REST API rule.