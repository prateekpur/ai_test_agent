# Phase 2 Generator

Implemented: ✅

## What Was Built

A template-based code generator that converts test plans into pytest-playwright test files.

## Features

- **Template-Based:** Uses predefined templates for each action type
- **Type-Safe:** Generates properly typed pytest-playwright code
- **Clean Output:** Formatted, readable test code with proper imports
- **Flexible:** Supports single or multiple tests per file
- **Validated:** All generated code passes Python syntax validation

## Supported Actions

| Action | Template | Example |
|--------|----------|---------|
| `navigate` | `page.goto(url)` | Navigate to URL |
| `fill` | `page.fill(selector, value)` | Fill form input |
| `click` | `page.click(selector)` | Click element |
| `assert_visible` | `expect(locator).to_be_visible()` | Assert element visible |
| `assert_text` | `expect(locator).to_contain_text(text)` | Assert text content |

## API

### `generate_web_tests(plan, output_dir) -> List[str]`

Generate a single test file from a plan.

**Returns:** List containing the generated file path

### `generate_test_code(plan) -> str`

Generate test code as a string (no file I/O).

**Returns:** Complete test code with imports

### `generate_multiple_tests(plans, output_dir) -> List[str]`

Generate multiple tests in a single file.

**Returns:** List containing the generated file path

## Usage

```python
from src.agents.planner import plan_tests
from src.agents.generator import generate_web_tests

context = {"base_url": "https://example.com"}
plan = plan_tests("test user login", context)

files = generate_web_tests(plan, "output/tests")
print(f"Generated: {files[0]}")
```

## Example Output

**Input Plan:**
```python
{
    "test_name": "test_login_flow",
    "steps": [
        {"action": "navigate", "url": "https://example.com/login"},
        {"action": "fill", "selector": "#username", "value": "admin"},
        {"action": "click", "selector": "button[type='submit']"},
        {"action": "assert_visible", "selector": ".dashboard"}
    ]
}
```

**Generated Code:**
```python
from playwright.sync_api import Page, expect


def test_login_flow(page: Page):
    page.goto("https://example.com/login")
    page.fill("#username", "admin")
    page.click("button[type='submit']")
    expect(page.locator(".dashboard")).to_be_visible()
```

## Implementation Details

### Template System

```python
class ActionTemplate:
    NAVIGATE = '    page.goto("{url}")'
    FILL = '    page.fill("{selector}", "{value}")'
    CLICK = '    page.click("{selector}")'
    ASSERT_VISIBLE = '    expect(page.locator("{selector}")).to_be_visible()'
    ASSERT_TEXT = '    expect(page.locator("{selector}")).to_contain_text("{contains}")'
```

### Code Generation Process

1. Parse plan structure
2. Map each step to appropriate template
3. Format template with step data
4. Combine steps into function body
5. Add imports and type hints
6. Write to file

## Files

```
src/agents/
├── generator.py         # Template-based generator
└── planner.py          # Plan creator (Phase 2)

examples/
├── generator_example.py    # Generator usage demo
└── integration_test.py     # Planner → Generator test
```

## Testing

```bash
# Run generator example
PYTHONPATH=. python3 examples/generator_example.py

# Run integration test
PYTHONPATH=. python3 examples/integration_test.py
```

## Validation

✅ **Syntax Check:** All generated code passes `py_compile`  
✅ **Type Safety:** Proper `Page` type hints  
✅ **Import Correctness:** `playwright.sync_api` imports work  
✅ **Integration:** Planner → Generator pipeline tested  

## Next Steps (Phase 2 Remaining)

- [ ] Implement Critic (`agents/critic.py`) to analyze test results
- [ ] Implement Fixer (`agents/fixer.py`) to log suggested fixes

## Phase 3 Upgrade Path

In Phase 3, optionally replace with LLM-based generator for:
- Natural language to code conversion
- Complex edge case handling
- Context-aware selector generation
- Smart assertion creation

The template-based approach remains valid for deterministic scenarios.
