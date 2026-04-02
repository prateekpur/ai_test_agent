# Phase 2 Critic

Implemented: ✅

## What Was Built

A regex-based test result analyzer that parses pytest output, classifies failures, and provides diagnostic information (no LLM).

## Features

- **Failure Classification:** Identifies 7 failure types using pattern matching
- **Test Parsing:** Extracts test counts, failed test names, errors, and line numbers
- **Smart Diagnosis:** Generates human-readable failure descriptions
- **Fix Suggestions:** Provides actionable recommendations for each failure type

## Supported Failure Types

| Type | Description | Example Pattern |
|------|-------------|-----------------|
| `timeout` | Element not found within timeout | `Timeout 30000ms exceeded` |
| `locator_not_found` | Selector not found in DOM | `Target closed`, `No element found` |
| `element_disappeared` | Element removed during test | `Element is not attached to the DOM` |
| `assertion` | Assertion failed | `AssertionError`, `Expected X but received Y` |
| `network` | Network/connection error | `net::ERR_`, `Failed to fetch` |
| `playwright_error` | Playwright API error | `BrowserContext is closed` |
| `unknown` | Unclassified error | Falls back when no pattern matches |

## API

### `analyze_test_results(stdout, stderr, return_code) -> dict`

Analyze test execution results.

**Returns:**
```python
{
    "status": str,              # "passed", "failed", or "error"
    "return_code": int,         # Process exit code
    "total_tests": int,         # Total test count
    "passed": int,              # Passed test count
    "failed": int,              # Failed test count
    "failure_type": str,        # Classified failure type (or None)
    "failed_tests": [           # List of failed test details
        {
            "file": str,        # Test file path
            "name": str,        # Test function name
            "error": str,       # Error message
            "line": int         # Line number (if available)
        }
    ],
    "diagnosis": str,           # Human-readable diagnosis
    "suggested_fix": str        # Actionable fix suggestion (or None)
}
```

### `print_analysis(analysis) -> None`

Pretty-print analysis results to console.

## Usage

```python
from src.agents.critic import analyze_test_results, print_analysis
from src.runners.web_runner import run_web_tests

# Run tests
result = run_web_tests(test_dir="output/tests")

# Analyze results
analysis = analyze_test_results(result.stdout, result.stderr, result.return_code)

# Print report
print_analysis(analysis)

# Programmatic access
if analysis["failed"] > 0:
    print(f"Failure type: {analysis['failure_type']}")
    for test in analysis["failed_tests"]:
        print(f"  {test['name']}: {test['error']}")
```

## Example Output

**Passing Tests:**
```
Status: passed
Passed: 3
Failed: 0
```

**Failed Test:**
```
============================================================
Test Analysis Report
============================================================
Status: FAILED
Return Code: 1
Total Tests: 2
Passed: 1
Failed: 1

Failure Type: timeout

Failed Tests:
  - test_login_flow
    File: test_login.py
    Line: 8
    Error: playwright._impl._api_types.TimeoutError: Timeout 30000ms exceeded.

Diagnosis:
  Test(s) timed out: test_login_flow. Element(s) not found or action took too long.

Suggested Fix:
  Increase timeout parameter or add explicit wait (wait_for_selector, wait_for_load_state)
============================================================
```

## Fix Suggestion Mapping

```python
timeout → "Increase timeout parameter or add explicit wait"
locator_not_found → "Verify selector exists in DOM, try alternative selectors"
element_disappeared → "Element removed from DOM - add stability checks"
assertion → "Review expected vs actual values"
network → "Check if application is running and URL is correct"
playwright_error → "Check browser/context lifecycle"
```

## Implementation Details

### Pattern Matching

Uses regex patterns to identify failure types:

```python
FAILURE_PATTERNS = {
    "timeout": [
        r"Timeout \d+ms exceeded",
        r"TimeoutError",
        r"page\.waitFor.*: Timeout",
    ],
    "assertion": [
        r"AssertionError",
        r"expect\(.*\)\..*: Expected",
    ],
    ...
}
```

### Parsing Strategy

1. Extract test counts from pytest summary line
2. Find failed test markers (`FAILED file.py::test_name`)
3. Extract error messages from failure sections
4. Match error patterns to classify failure type
5. Generate diagnosis based on classification

## Files

```
src/agents/
├── critic.py            # Main critic implementation
└── CRITIC.md           # This file

examples/
├── critic_example.py       # Usage demo
└── critic_unit_tests.py    # Unit tests
```

## Testing

```bash
# Run unit tests
PYTHONPATH=. python3 examples/critic_unit_tests.py

# Run integration example (requires generated tests)
PYTHONPATH=. python3 examples/critic_example.py
```

## Validation

✅ **Unit Tests:** All 4 test scenarios pass  
✅ **Pattern Matching:** Correctly identifies timeout, assertion, locator errors  
✅ **Parsing Accuracy:** Extracts test names, files, line numbers  
✅ **Diagnosis Quality:** Generates clear, actionable messages  

## Next Steps (Phase 2)

- [ ] Implement Fixer (`agents/fixer.py`) to log suggested code changes

## Phase 3 Upgrade Path

In Phase 3, optionally replace with LLM-based critic for:
- Natural language error analysis
- Context-aware fix suggestions
- Learning from past failures
- Complex multi-error diagnosis
- Smart test improvement recommendations

The regex-based approach remains valid for fast, deterministic analysis.
