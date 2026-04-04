from typing import Any, Dict, List

FIX_STRATEGIES = {
    "timeout": {
        "title": "Timeout Issues",
        "strategies": [
            {
                "description": "Increase timeout parameter",
                "before": "page.click(selector)",
                "after": "page.click(selector, timeout=60000)",
                "priority": "High",
            },
            {
                "description": "Add explicit wait before action",
                "before": "page.click(selector)",
                "after": "page.wait_for_selector(selector, state='visible')\npage.click(selector)",
                "priority": "Medium",
            },
            {
                "description": "Wait for network idle",
                "before": "page.goto(url)\npage.click(selector)",
                "after": "page.goto(url)\npage.wait_for_load_state('networkidle')\npage.click(selector)",
                "priority": "Low",
            },
        ],
        "general_tips": [
            "Check if element is dynamically loaded",
            "Verify selector in browser DevTools",
            "Consider using wait_for_function() for complex conditions",
        ],
    },
    "locator_not_found": {
        "title": "Locator Not Found",
        "strategies": [
            {
                "description": "Use data-testid attribute",
                "before": "page.click('#dynamic-id-123')",
                "after": "page.get_by_test_id('submit-button').click()",
                "priority": "High",
            },
            {
                "description": "Use text-based selector",
                "before": "page.click('.submit')",
                "after": "page.get_by_text('Submit').click()",
                "priority": "High",
            },
            {
                "description": "Use role-based selector",
                "before": "page.click('#submit')",
                "after": "page.get_by_role('button', name='Submit').click()",
                "priority": "High",
            },
            {
                "description": "Add wait_for_selector",
                "before": "page.click(selector)",
                "after": "page.wait_for_selector(selector)\npage.click(selector)",
                "priority": "Medium",
            },
        ],
        "general_tips": [
            "Verify selector exists using browser DevTools",
            "Check if element is in shadow DOM or iframe",
            "Try multiple selector alternatives",
        ],
    },
    "element_disappeared": {
        "title": "Element Disappeared",
        "strategies": [
            {
                "description": "Wait for network idle before interaction",
                "before": "page.goto(url)\npage.click(selector)",
                "after": "page.goto(url)\npage.wait_for_load_state('networkidle')\npage.click(selector)",
                "priority": "High",
            },
            {
                "description": "Add stability check",
                "before": "page.click(selector)",
                "after": "page.wait_for_selector(selector, state='attached')\npage.click(selector)",
                "priority": "Medium",
            },
        ],
        "general_tips": [
            "Element may be removed/replaced by JavaScript",
            "Check for dynamic content updates",
            "Use more stable parent selectors",
        ],
    },
    "assertion": {
        "title": "Assertion Failures",
        "strategies": [
            {
                "description": "Add debugging to see actual value",
                "before": "expect(page.locator(selector)).to_contain_text('Expected')",
                "after": "actual = page.locator(selector).text_content()\nprint(f'Actual value: {actual}')\nexpect(page.locator(selector)).to_contain_text('Expected')",
                "priority": "High",
            },
            {
                "description": "Use softer assertion",
                "before": "expect(page.locator(selector)).to_have_text('Exact Text')",
                "after": "expect(page.locator(selector)).to_contain_text('Text')",
                "priority": "Medium",
            },
        ],
        "general_tips": [
            "Verify expected values match application behavior",
            "Check if test data needs updating",
            "Consider using regex for flexible matching",
        ],
    },
    "network": {
        "title": "Network Errors",
        "strategies": [
            {
                "description": "Verify application is running",
                "before": "page.goto('https://localhost:3000')",
                "after": "# Ensure application is running before tests\npage.goto('https://localhost:3000')",
                "priority": "High",
            },
            {
                "description": "Add retry logic",
                "before": "page.goto(url)",
                "after": "page.goto(url, wait_until='networkidle', timeout=60000)",
                "priority": "Medium",
            },
        ],
        "general_tips": [
            "Check if base URL is correct",
            "Verify application is accessible",
            "Check network connectivity",
        ],
    },
    "playwright_error": {
        "title": "Playwright API Errors",
        "strategies": [
            {
                "description": "Check browser context lifecycle",
                "before": "# Context may be closed prematurely",
                "after": "# Ensure browser context is not closed before test completes",
                "priority": "High",
            },
        ],
        "general_tips": [
            "Review test setup and teardown",
            "Check conftest.py fixtures",
            "Verify browser instance management",
        ],
    },
    "unknown": {
        "title": "Unknown Errors",
        "strategies": [
            {
                "description": "Add detailed error logging",
                "before": "page.click(selector)",
                "after": "try:\n    page.click(selector)\nexcept Exception as e:\n    print(f'Error details: {e}')\n    raise",
                "priority": "High",
            },
        ],
        "general_tips": [
            "Review full error stack trace",
            "Check pytest output for details",
            "Add debug logging to test",
        ],
    },
}


def fix_tests(diagnosis: Dict[str, Any], test_files: List[str]) -> None:
    print("=" * 60)
    print("Fixer Recommendations")
    print("=" * 60)
    print(f"Status: {diagnosis['status'].upper()}")

    if diagnosis["status"] == "passed":
        print("\n✓ All tests passed - no fixes needed")
        print("=" * 60)
        return

    failure_type = diagnosis.get("failure_type", "unknown")
    failed_tests = diagnosis.get("failed_tests", [])

    print(f"Failure Type: {failure_type}")
    print(f"Failed Tests: {len(failed_tests)}")
    print()

    strategies_info = _get_fix_strategies(failure_type)

    for test in failed_tests:
        print("=" * 60)
        print(f"Test: {test['file']}::{test['name']}", end="")
        if test.get("line"):
            print(f" (Line {test['line']})")
        else:
            print()
        print(f"Error: {test['error'][:80]}...")
        print("=" * 60)
        print()

        print(f"Fix Strategies for {strategies_info['title']}:")
        print()

        for i, strategy in enumerate(strategies_info["strategies"], 1):
            _print_strategy(strategy, i)

        print("\nGeneral Tips:")
        for tip in strategies_info["general_tips"]:
            print(f"  • {tip}")

        print()
        print("=" * 60)
        print()

    print("Would fix files:")
    unique_files = {test["file"] for test in failed_tests}
    for filepath in unique_files:
        test_count = sum(1 for t in failed_tests if t["file"] == filepath)
        print(f"  ✓ {filepath} ({test_count} test(s))")

    print()
    print("Summary:")
    print(f"  • {len(failed_tests)} test(s) would be analyzed")
    print(
        f"  • {len(strategies_info['strategies'])} fix strateg{'ies' if len(strategies_info['strategies']) > 1 else 'y'} available"
    )
    print("  • No files were actually modified (Phase 2 dummy mode)")
    print()
    print("=" * 60)


def _get_fix_strategies(failure_type: str) -> Dict[str, Any]:
    return FIX_STRATEGIES.get(failure_type, FIX_STRATEGIES["unknown"])


def _print_strategy(strategy: Dict[str, str], index: int) -> None:
    print(f"Strategy {index}: {strategy['description']} (Priority: {strategy['priority']})")
    print("─" * 60)

    print("\n  Before:")
    for line in strategy["before"].split("\n"):
        print(f"    {line}")

    print("\n  After:")
    for line in strategy["after"].split("\n"):
        print(f"    {line}")

    print()
