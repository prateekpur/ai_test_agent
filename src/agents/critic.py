import re
from typing import Any, Dict, List

FAILURE_PATTERNS = {
    "timeout": [
        r"Timeout \d+ms exceeded",
        r"TimeoutError",
        r"page\.waitFor.*: Timeout",
        r"locator\..*: Timeout \d+ms exceeded",
        r"expect\(.*\)\..*: Timeout",
    ],
    "locator_not_found": [
        r"locator\..*: Target closed",
        r"No element found",
        r"Selector '.*' resolved to hidden",
        r"Selector '.*' did not match any elements",
        r"Error: locator\..*: Expected",
    ],
    "element_disappeared": [
        r"Target closed",
        r"Element is not attached to the DOM",
        r"Node is detached from document",
    ],
    "assertion": [
        r"AssertionError",
        r"expect\(.*\)\..*: Expected .* but received",
        r"assert .* == .*",
        r"Expected .* to be .*",
    ],
    "network": [
        r"net::ERR_",
        r"NetworkError",
        r"Failed to fetch",
        r"ERR_CONNECTION_REFUSED",
        r"ERR_NAME_NOT_RESOLVED",
    ],
    "playwright_error": [
        r"playwright\._impl\._api_types\.Error",
        r"BrowserContext is closed",
        r"Page is closed",
    ],
}

FIX_SUGGESTIONS = {
    "timeout": "Increase timeout parameter or add explicit wait (wait_for_selector, wait_for_load_state)",
    "locator_not_found": "Verify selector exists in DOM, try alternative selectors (data-testid, text, role)",
    "element_disappeared": "Element removed from DOM - add stability checks or wait_for_selector before interaction",
    "assertion": "Review expected vs actual values, check if element text/visibility changed",
    "network": "Check if application is running and URL is correct",
    "playwright_error": "Check browser/context lifecycle - may need to recreate browser instance",
    "unknown": "Review full error message and stack trace for details",
}


def analyze_test_results(stdout: str, stderr: str, return_code: int) -> Dict[str, Any]:
    combined_output = stdout + "\n" + stderr

    passed = _extract_passed_count(stdout)
    failed = _extract_failed_count(stdout)
    total = passed + failed

    failed_tests = _extract_failed_tests(stdout)

    failure_type = _classify_failure(combined_output)

    diagnosis = _generate_diagnosis(failure_type, failed_tests, combined_output)

    suggested_fix = FIX_SUGGESTIONS.get(failure_type, FIX_SUGGESTIONS["unknown"])

    status = "passed" if return_code == 0 else ("failed" if failed > 0 else "error")

    return {
        "status": status,
        "return_code": return_code,
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "failure_type": failure_type if failed > 0 else None,
        "failed_tests": failed_tests,
        "diagnosis": diagnosis,
        "suggested_fix": suggested_fix if failed > 0 else None,
    }


def _extract_passed_count(output: str) -> int:
    match = re.search(r"(\d+) passed", output)
    return int(match.group(1)) if match else 0


def _extract_failed_count(output: str) -> int:
    match = re.search(r"(\d+) failed", output)
    return int(match.group(1)) if match else 0


def _extract_failed_tests(output: str) -> List[Dict[str, Any]]:
    failed_tests = []

    for match in re.finditer(r"FAILED (.*?)::(.*?)(?:\s|$)", output):
        file_path = match.group(1)
        test_name = match.group(2)

        error = _extract_error_for_test(output, test_name)
        line_number = _extract_line_number(output, test_name)

        failed_tests.append(
            {
                "file": file_path,
                "name": test_name,
                "error": error,
                "line": line_number,
            }
        )

    return failed_tests


def _extract_error_for_test(output: str, test_name: str) -> str:
    pattern = rf"{test_name}.*?E\s+(.*?)(?:\n\n|\ntest_|\Z)"
    match = re.search(pattern, output, re.DOTALL)

    if match:
        error_text = match.group(1).strip()
        error_lines = [line.strip() for line in error_text.split("\n") if line.strip()]
        return " ".join(error_lines[:3])

    return "Unknown error"


def _extract_line_number(output: str, test_name: str) -> int:
    pattern = rf"{test_name}.*?:(\d+):"
    match = re.search(pattern, output)
    return int(match.group(1)) if match else 0


def _classify_failure(output: str) -> str:
    for failure_type, patterns in FAILURE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, output, re.IGNORECASE):
                return failure_type

    return "unknown"


def _generate_diagnosis(failure_type: str, failed_tests: List[Dict[str, Any]], output: str) -> str:
    if not failed_tests:
        return "All tests passed successfully"

    test_count = len(failed_tests)
    test_names = ", ".join([t["name"] for t in failed_tests[:3]])
    if test_count > 3:
        test_names += f" and {test_count - 3} more"

    diagnoses = {
        "timeout": f"Test(s) timed out: {test_names}. Element(s) not found or action took too long.",
        "locator_not_found": f"Selector(s) not found in {test_names}. Element may not exist or selector is incorrect.",
        "element_disappeared": f"Element disappeared during test execution in {test_names}. DOM changed unexpectedly.",
        "assertion": f"Assertion failed in {test_names}. Expected value did not match actual value.",
        "network": f"Network error in {test_names}. Application may not be running or URL is incorrect.",
        "playwright_error": f"Playwright API error in {test_names}. Browser/context may be closed.",
        "unknown": f"Unknown error in {test_names}. Review detailed output for more information.",
    }

    return diagnoses.get(failure_type, diagnoses["unknown"])


def print_analysis(analysis: Dict[str, Any]) -> None:
    print("=" * 60)
    print("Test Analysis Report")
    print("=" * 60)
    print(f"Status: {analysis['status'].upper()}")
    print(f"Return Code: {analysis['return_code']}")
    print(f"Total Tests: {analysis['total_tests']}")
    print(f"Passed: {analysis['passed']}")
    print(f"Failed: {analysis['failed']}")
    print()

    if analysis["failed"] > 0:
        print(f"Failure Type: {analysis['failure_type']}")
        print()
        print("Failed Tests:")
        for test in analysis["failed_tests"]:
            print(f"  - {test['name']}")
            print(f"    File: {test['file']}")
            if test.get("line"):
                print(f"    Line: {test['line']}")
            print(f"    Error: {test['error']}")
            print()

        print("Diagnosis:")
        print(f"  {analysis['diagnosis']}")
        print()
        print("Suggested Fix:")
        print(f"  {analysis['suggested_fix']}")
    else:
        print("All tests passed successfully!")

    print("=" * 60)
