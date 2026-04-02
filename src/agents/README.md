# Phase 2 Fake Planner

Implemented: ✅

## What Was Built

A hard-coded test planner that returns pre-defined test plans based on keyword matching (no LLM).

## Features

- **7 Test Scenarios:** Login, Search, Checkout, Forms, Registration, Navigation, Generic
- **Keyword Matching:** Analyzes description to select appropriate plan
- **Structured Output:** Returns standardized test plan format for generator consumption
- **Flexible Selectors:** Includes multiple selector options for robustness

## Test Plan Structure

```python
{
    "test_name": str,           # Test function name
    "description": str,         # Human-readable description
    "steps": [                  # Ordered test steps
        {
            "action": str,      # navigate, fill, click, assert_visible, assert_text
            "selector": str,    # CSS selector (optional)
            "url": str,         # URL path (optional)
            "value": str,       # Input value (optional)
            "contains": str,    # Text assertion (optional)
            "description": str  # Step description
        }
    ],
    "setup": {
        "viewport": {"width": int, "height": int},
        "browser": str
    }
}
```

## Supported Actions

- `navigate` - Go to URL
- `fill` - Enter text into input field
- `click` - Click element
- `assert_visible` - Verify element is visible
- `assert_text` - Verify element contains text

## Usage

```python
from src.agents.planner import plan_tests, get_supported_scenarios

context = {
    "base_url": "https://example.com",
    "browser": "chromium"
}

plan = plan_tests("test user login flow", context)
print(plan["test_name"])  # test_login_flow
print(len(plan["steps"]))  # 5
```

## Example Output

**Input:** `"test user login flow"`

**Output:**
```python
{
    "test_name": "test_login_flow",
    "description": "test user login flow",
    "steps": [
        {"action": "navigate", "url": "https://example.com/login", ...},
        {"action": "fill", "selector": "#username", "value": "testuser@example.com", ...},
        {"action": "fill", "selector": "#password", "value": "password123", ...},
        {"action": "click", "selector": "button[type='submit']", ...},
        {"action": "assert_visible", "selector": ".user-profile, .dashboard", ...}
    ],
    "setup": {"viewport": {"width": 1280, "height": 720}, "browser": "chromium"}
}
```

## Files

```
src/agents/
├── __init__.py          # Package exports
├── planner.py           # Main planner implementation
└── README.md           # This file

examples/
└── planner_example.py  # Usage demonstration
```

## Testing

```bash
PYTHONPATH=/Users/prateekpuri/ai_agent/ai_test_agent python3 examples/planner_example.py
```

## Next Steps (Phase 2 Remaining)

- [ ] Implement Generator (`agents/generator.py`) to convert plans to pytest-playwright code
- [ ] Implement Critic (`agents/critic.py`) to analyze test results
- [ ] Implement Fixer (`agents/fixer.py`) to log suggested fixes

## Phase 3 Upgrade Path

In Phase 3, replace this fake planner with LLM-based planner:
- Parse natural language descriptions with AI
- Generate dynamic plans for any test scenario
- Support complex multi-step flows
- No keyword matching limitations
