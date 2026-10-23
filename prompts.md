# Prompts Log

Prompts are documented in the order they were used. Original prompts are preserved exactly as entered. Results, observations, and validation outcomes are documented separately from the prompt text.

Final suite status (confirmed 2026-10-23): `python -m pytest` collects and passes all tests: 5 Login, 5 Dashboard, 7 REST API, 2 example tests.

## Login Module

### Prompt v1: Initial Test Case Generation

**Tool:** Claude
**Date:** 2026-10-22

**Prompt:**

Generate test cases for the login page of a web app. Cover valid login, invalid credentials, forgot password, session expiry and brute-force lockout.

#### v1 Result

**Raw output:** `generated_tests/raw/login_v1_output.md`

**Problems identified:**

- Markdown tables with free-text steps, not Gherkin or JSON, so not directly automatable.
- About 65 cases, and the output was cut off mid-row at BF-15 because no size limit was set.
- Many expected results were hedged ("per spec", "or a validation message").
- No concrete test data, and no priority or tags.
- Included features SauceDemo doesn't have (email login, forgot password, remember me, CAPTCHA).

**Conclusion:** The prompt did not provide enough application context or define a strict, automation-friendly output format. Prompt v2 was created to address these issues.

### Prompt v2: Refined Gherkin Generation

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
- Clarified that unsupported SauceDemo features should not be invented, so the model used `@design-only` and proxies (locked_out_user, cookie deletion).
- Required concrete test data, deterministic expected outcomes, and a coverage check.

**Remaining issues identified during review:**

- Error messages and the cookie name came from the model and needed verification against the live site. I checked the error messages and the `/inventory.html` redirect in the browser before writing automation.
- BF-04 was tagged `@automatable` while also carrying a comment that the functionality was not present. This inconsistency was noted but not changed in the saved file.

**Conclusion:** Prompt v2 improved the structure and relevance of the generated cases, but the output still needed manual verification.

### Prompt v3: Login UI Automation

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

(Note: the duplicated "Task / TASK" heading is in the prompt exactly as I sent it.)

#### v3 Result

**Output:** `tests/ui/test_login.py`

**Validation command:** `python -m pytest tests/ui/test_login.py -v`

**Validation result:** All five Login tests passed (terminal output recorded 2026-10-22, and again in the full-suite run on 2026-10-23).

**What worked:**

- Implemented five Login scenarios using Python, Playwright, and pytest.
- Verified exact error messages for negative Login scenarios.
- Verified successful navigation to the inventory page.

#### Login module note

- v1 failed on format, length (output truncated), hedged outcomes and invented features.
- v2 added role, app context, a strict Gherkin format with tags, a scenario cap, and an explicit "do not invent features" rule with `@design-only` for missing ones.
- v2 still needed human verification: the error messages and redirect were checked on the live site, and the BF-04 tag inconsistency was left as a recorded finding.
- v3 asked only for scenarios I had verified by hand, which is why all five tests passed first time.

---

## Dashboard Module

### Prompt v1: Dashboard UI Automation

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

1. `test_inventory_page_displays_products`: product names and prices are visible.
2. `test_inventory_displays_six_products`: six products are displayed.
3. `test_inventory_can_be_sorted_by_price_low_to_high`: ascending price sorting.
4. `test_adding_product_updates_cart_badge`: cart badge and Remove button after adding a product.
5. `test_shopping_cart_navigation_opens_cart_page`: navigation to the cart page and its heading.

**Review observations:**

- The tests use a fixture to log in before checking inventory functionality.
- The first test contains a somewhat redundant nonzero product-count assertion.
- The code was run in headed mode with slow motion so browser actions could be observed.

**Validation result:** All five Dashboard tests passed in the full-suite run on 2026-10-23.

### Prompt G1: Dashboard test case generation (naive)

**Tool:** Claude
**Date:** 2026-10-23

**Prompt:**

Generate test cases for the dashboard of a web app. Cover widget loading, data accuracy, filter/sort behavior, responsive layout and permission-based visibility.

#### G1 Result

**Raw output:** `generated_tests/raw/dashboard_v1_output.md`

**Problems identified:**

- Markdown tables with free-text steps, not Gherkin or JSON, so not directly automatable.
- About 65 cases across six tables, with no cap, so far too many to implement or review.
- Invented a generic dashboard (KPI cards, charts, roles Admin/Manager/Viewer, multi-tenant orgs) that does not exist on SauceDemo.
- Many cases need things I can't do on the target: database queries, mocking a 500, 100k records, multiple IPs and orgs, Safari.
- Hedged outcomes ("per spec", "inclusive or exclusive", "or 404") that can't be asserted.
- No concrete test data and no tags, so nothing separates smoke from edge cases.
- Not tied to the SauceDemo inventory page, which is what my automated tests actually cover.

### Prompt G2: Dashboard test case generation (grounded in SauceDemo)

**Tool:** Claude
**Date:** 2026-10-23

**Prompt:**

ROLE
You are a senior SDET writing automatable regression tests for a web app.

CONTEXT
App under test: https://www.saucedemo.com (stand-in for a test management platform dashboard).
After login as standard_user / secret_sauce, the page /inventory.html shows:
- 6 product cards, each with name, description, price, image and an "Add to cart" button (it becomes "Remove" once clicked)
- A sort dropdown with: Name (A to Z), Name (Z to A), Price (low to high), Price (high to low)
- A cart icon in the header with a badge showing the item count
- A burger menu with All Items, About, Logout, Reset App State
There are NO widgets, charts, date filters, text filters, pagination, user roles or admin views.
Other users: problem_user (known to behave differently from standard_user), locked_out_user (cannot log in). Password for all: secret_sauce.

TASK
Generate test cases for these five areas: widget loading (product cards loading), data accuracy, filter/sort behavior, responsive layout, permission-based visibility.

OUTPUT FORMAT
- Gherkin only. One Feature per area (5 Features total). No commentary before or after.
- Every Scenario starts with a tag line: @id-WL-01 (prefix WL, DA, FS, RL, PV), a priority (@P1, @P2, @P3), a type (@positive, @negative, @boundary, @security), and @automatable or @design-only.
- Max 6 steps per scenario. Use concrete test data (exact product names, prices, viewport sizes), never "valid data".
- Each Then step must be one deterministic, assertable outcome. No "or", no "per spec".

RULES
- 4 to 6 scenarios per area, no more. No duplicates.
- Do not invent UI elements, products, prices or text. If you are not sure of an exact value, use a step that reads it from the page instead of hard-coding it.
- If an area cannot be tested on this app (permission-based visibility by role, filters beyond the sort dropdown), write those scenarios as @design-only and add a one-line comment "# Not present on SauceDemo: <reason>". Where a realistic proxy exists (e.g. unauthenticated access to /inventory.html for permissions, problem_user for behavioural differences, browser viewport resizing for responsive layout), write an @automatable scenario using it.
- No scenarios that need a database, mocked API failures, multiple browsers, or waits over 10 seconds.

EXAMPLE OF EXPECTED STYLE
@id-FS-01 @P1 @positive @automatable
Scenario: Sort products by price low to high
  Given I am logged in as "standard_user" with password "secret_sauce"
  When I select "Price (low to high)" in the sort dropdown
  Then the product prices are in ascending order

SELF-CHECK
After the Gherkin, add a short comment block "# COVERAGE CHECK" listing, per area, the number of scenarios and any requirement you could not cover and why.

#### G2 Result

**Output:** `generated_tests/dashboard.feature`

**Improvements over G1:**

- Gherkin with tags, 5 to 6 scenarios per area, concrete SauceDemo data (names, prices, viewport sizes).
- Grounded in the real inventory page, so no invented widgets, roles or charts.
- Permission-based visibility was reframed as authentication and access, and marked `@design-only` where only manual checks apply.

**Problems identified:**

- The prompt was sent in full, but the model reported that its RULES section was cut off after "If an area cannot be". The output has a `# NOTE` line and no `# COVERAGE CHECK` block, so the later rules were probably not applied.
- A few `Then` steps assert more than one outcome (WL-02, DA-02, RL-01), against the "one assertable outcome" rule.
- Product names and prices were hard-coded from the model's memory rather than read from the page. I need to verify them on the live site.

**What I would change in G3:** shorten the prompt so it is not clipped, put the most important rules (no commentary, one outcome per Then, coverage check) near the top, and re-run.

#### Dashboard module note

- The automation prompt asked for tests "based only on behavior that can be verified", so it did not invent widgets and SauceDemo's inventory page was treated as the dashboard stand-in.
- G1 failed on format, size and an invented app. G2 added SauceDemo context, Gherkin and tags, which fixed those.
- The RULES section was reported as cut off, so the output missed the no-commentary and coverage-check rules, and a few `Then` steps still assert more than one outcome.
- Permission-based visibility has no real equivalent on SauceDemo, so it is covered through authentication scenarios. Responsive layout and permissions exist only as Gherkin, not as automated tests.

---

## REST API Module

### Prompt v1: API Test Design (Gherkin)

**Tool:** ChatGPT
**Date:** 2026-10-22

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

#### API v1 Result

**Output:** `generated_tests/raw/api_tests.feature`

**Problems identified:**

- Scenarios lack per-scenario test IDs, objectives and explicit preconditions/request data, even though the prompt asked for them.
- Some expected outcomes are ambiguous (for example "200 or 204"), which can't be asserted.
- Coverage of invalid field values and error-format consistency is thin.
- The prompt targets a hypothetical API, so the design is generic and not tied to the endpoints I actually tested.

### Prompt v2: API Test Implementation

**Tool:** ChatGPT
**Date:** 2026-10-22

**Prompt:**

<PASTE THE EXACT PROMPT YOU GAVE CHATGPT TO WRITE tests/api/test_rest_api.py. If you don't have it, write "Original prompt not saved" here. Do not reconstruct it.>

#### API v2 Result

**Output:** `tests/api/test_rest_api.py`

**Tests generated (JSONPlaceholder):** GET list, GET single post with schema check, POST, PUT, PATCH, DELETE, GET nonexistent post.

**Refinement during validation:**

- **Initial attempt:** the nonexistent-resource test assumed `GET /posts/999999` returns HTTP 200 with an empty JSON object.
- **Observed failure:** the API returned HTTP 404, so the assertion failed, and the Failure Explainer produced an explanation of the mismatch.
- **Fix:** I changed the expected status to 404 based on the observed response. This finding applies to this public API endpoint and is not a universal REST rule.

**Validation result:** All seven API tests passed in the full-suite run on 2026-10-23.

#### API module note

- The first prompt asked for a design for a hypothetical API, which produced generic scenarios with ambiguous outcomes ("200 or 204") and missing IDs.
- I changed approach: test a real public API (JSONPlaceholder) so expected statuses could be observed instead of assumed.
- A wrong assumption (200 for a missing post) was caught by a failing test and corrected to 404.
- Not covered against the real API: token validation and rate limiting, because JSONPlaceholder has neither. They remain design-level scenarios in `api_tests.feature`.

---

## Task 3: Failure Explainer (Option A)

### Implementation prompt

**Tool:** ChatGPT
**Date:** 2026-10-22

**Prompt:**

<PASTE THE EXACT PROMPT YOU GAVE CHATGPT TO BUILD THE FAILURE EXPLAINER. If it's not saved, write "Original prompt not saved".>

### Runtime prompt sent to Gemini

The prompt sent to the LLM at test-failure time lives in `ai/prompt_templates.py` (`FAILURE_EXPLAINER_PROMPT`):

<PASTE THE CONTENTS OF FAILURE_EXPLAINER_PROMPT HERE, exactly as it appears in the file>

#### Result

- Real Gemini API call on every failing test; explanations are printed to the terminal and saved to `reports/sample_output/failure_explanations.txt`.
- Failure text is redacted for keys, tokens and passwords before being sent, then truncated to 6,000 characters.
- Sample output was produced from a deliberate demo failure and from the real 404 assertion failure in the API tests.

#### Failure Explainer note

- The first version only saved explanations to a file, so a failure on screen showed no explanation. I added terminal printing.
- The first version loaded the key from `.env.example`, which got a real key committed locally. GitHub push protection blocked the push. I revoked the key, rewrote the local commit, and moved loading to the ignored `.env`.
- The first version sent raw failure text. I added redaction before truncation.
- Explanations are hypotheses and are not verified automatically.