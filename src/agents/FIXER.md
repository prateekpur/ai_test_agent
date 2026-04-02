# Phase 2 Fake Fixer

Implemented: ✅

## What Was Built

A log-based test fixer that analyzes failure diagnoses from the Critic and prints fix recommendations without modifying files (Phase 2 dummy mode).

## Features

- **7 Failure Type Strategies:** timeout, locator_not_found, element_disappeared, assertion, network, playwright_error, unknown
- **Prioritized Fix Strategies:** Each strategy marked as High/Medium/Low priority
- **Before/After Examples:** Shows code transformations for each fix
- **General Tips:** Additional guidance for each failure type
- **No File Modification:** Phase 2 implementation only logs recommendations

## Fix Strategy Structure

```python
{
    "title": str,                # Human-readable failure type
    "strategies": [              # List of fix approaches
        {
            "description": str,  # What this fix does
            "before": str,       # Original code pattern
            "after": str,        # Fixed code pattern
            "priority": str      # High/Medium/Low
        }
    ],
    "general_tips": [str]        # Additional guidance
}
```

## Supported Failure Types

### 1. Timeout
- Increase timeout parameter
- Add explicit wait before action
- Wait for network idle

### 2. Locator Not Found
- Use data-testid attribute
- Use text-based selector
- Use role-based selector
- Add wait_for_selector

### 3. Element Disappeared
- Wait for network idle before interaction
- Add stability check

### 4. Assertion
- Add debugging to see actual value
- Use softer assertion

### 5. Network
- Verify application is running
- Add retry logic

### 6. Playwright Error
- Check browser context lifecycle

### 7. Unknown
- Add detailed error logging

## Usage

```python
from src.agents.critic import analyze_test_results
from src.agents.fixer import fix_tests

diagnosis = analyze_test_results(stdout, stderr, return_code)
fix_tests(diagnosis, ["test_example.py"])
```

## Input Format (from Critic)

```python
{
    "status": "failed",
    "failure_type": "timeout",
    "total_tests": 1,
    "passed_tests": 0,
    "failed_tests": [
        {
            "file": "test_login.py",
            "name": "test_login_flow",
            "line": 15,
            "error": "Timeout 30000ms exceeded..."
        }
    ],
    "duration": "35.2s"
}
```

## Output Format

The fixer prints recommendations to stdout in a structured format:

```
============================================================
Fixer Recommendations
============================================================
Status: FAILED
Failure Type: timeout
Failed Tests: 1

============================================================
Test: test_login.py::test_login_flow (Line 15)
Error: Timeout 30000ms exceeded...
============================================================

Fix Strategies for Timeout Issues:

Strategy 1: Increase timeout parameter (Priority: High)
────────────────────────────────────────────────────────────

  Before:
    page.click(selector)

  After:
    page.click(selector, timeout=60000)

Strategy 2: Add explicit wait before action (Priority: Medium)
────────────────────────────────────────────────────────────

  Before:
    page.click(selector)

  After:
    page.wait_for_selector(selector, state='visible')
    page.click(selector)

...

General Tips:
  • Check if element is dynamically loaded
  • Verify selector in browser DevTools
  • Consider using wait_for_function() for complex conditions

============================================================

Would fix files:
  ✓ test_login.py (1 test(s))

Summary:
  • 1 test(s) would be analyzed
  • 3 fix strategies available
  • No files were actually modified (Phase 2 dummy mode)

============================================================
```

## Files

```
src/agents/
├── __init__.py          # Package exports (includes fix_tests)
├── fixer.py             # Main fixer implementation
└── FIXER.md            # This file

examples/
├── fixer_example.py    # Usage demonstration
└── fixer_unit_tests.py # 6 unit tests
```

## Testing

```bash
# Run example
PYTHONPATH=/Users/prateekpuri/ai_agent/ai_test_agent python3 examples/fixer_example.py

# Run unit tests
PYTHONPATH=/Users/prateekpuri/ai_agent/ai_test_agent python3 examples/fixer_unit_tests.py
```

## Phase 2 Completion

With this implementation, Phase 2 is now **100% complete**:
- ✅ Planner: Hard-coded test plans with keyword matching
- ✅ Generator: Template-based pytest-playwright code generation
- ✅ Critic: Regex-based failure analysis with 7 failure types
- ✅ Fixer: Log-based fix recommendations with prioritized strategies

## Phase 3 Upgrade Path

In Phase 3, replace this fake fixer with LLM-based fixer:
- Actually modify test files with fixes
- Use AI to understand context and apply appropriate fixes
- Support complex multi-line code transformations
- Learn from successful fixes over time
- Apply fixes automatically or interactively
