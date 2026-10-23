
import pytest
from pathlib import Path

from ai.failure_explainer import explain_failure

PROJECT_ROOT = Path(__file__).resolve().parent
REPORT_FILE = PROJECT_ROOT / "reports" / "sample_output" / "failure_explanations.txt"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Task 3 — Option A: Failure Explainer.
    Send actual pytest failure details to Gemini and save its explanation.
    """
    outcome = yield
    report = outcome.get_result()

    # Analyze actual test-call failures only; do not call Gemini for passing tests.
    if report.when == "call" and report.failed:
        failure_details = report.longreprtext or "No failure traceback available."

        explanation = explain_failure(
            test_name=report.nodeid,
            failure_details=failure_details,
        )

        REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

        report_entry = (
            f"\n{'=' * 70}\n"
            f"Test: {report.nodeid}\n"
            f"AI Failure Explanation:\n{explanation}\n"
        )

        # Display the explanation in the terminal.
        print(report_entry)

        # Save the same explanation in the report file.
        with REPORT_FILE.open("a", encoding="utf-8") as file:
            file.write(report_entry)
