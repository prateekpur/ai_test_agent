# Web Test Runner

Execute Playwright-based web tests using pytest.

## Installation

```bash
pip install -r src/requirements.txt
playwright install chromium
```

## Usage

### Configuration File (Recommended)

Create a `test_config.yaml` file:

```yaml
web:
  test_dir: "examples/web_tests"
  browser: "chromium"
  headed: false
  workers: null
  verbose: true
  timeout: 300
```

Then run tests using the config:

```python
from src.runners.web_runner import run_web_tests

# Load from config file
result = run_web_tests(config_path="config/test_config.yaml")

print(f"Status: {'PASSED' if result.success else 'FAILED'}")
print(result.stdout)
```

### Programmatic Usage (Direct Parameters)

```python
from src.runners.web_runner import run_web_tests

result = run_web_tests(
    test_dir="examples/web_tests",
    browser="chromium",
    headed=False,
    workers=None,
    verbose=True
)

print(f"Status: {'PASSED' if result.success else 'FAILED'}")
print(f"Return code: {result.return_code}")
print(result.stdout)
```

### Hybrid Usage (Config + Overrides)

```python
from src.runners.web_runner import run_web_tests

# Load config but override specific parameters
result = run_web_tests(
    config_path="config/test_config.yaml",
    browser="firefox",  # Override browser from config
    headed=True         # Override headed from config
)
```

### Command Line Example

```bash
python examples/run_web_tests.py
```

## API Reference

### `run_web_tests(config_path, test_dir, browser, headed, workers, verbose, timeout)`

Execute web tests from a directory.

**Parameters (all optional):**
- `config_path` (str): Path to YAML config file. Default: searches `config/test_config.yaml` and `test_config.yaml`
- `test_dir` (str): Path to directory containing test files. Overrides config value.
- `browser` (str): Browser to use (chromium, firefox, webkit). Overrides config value.
- `headed` (bool): Run in headed mode (visible browser). Overrides config value.
- `workers` (int): Number of parallel workers. Overrides config value.
- `verbose` (bool): Verbose output. Overrides config value.
- `timeout` (int): Test execution timeout in seconds. Overrides config value.

**Parameter Priority:**
1. Direct function parameters (highest)
2. Config file values
3. Built-in defaults (lowest)

**Returns:**
- `TestResult` object with:
  - `stdout` (str): Test output
  - `stderr` (str): Error output
  - `return_code` (int): Exit code (0 = success)
  - `success` (bool): True if tests passed
  - `failed` (bool): True if tests failed

**Raises:**
- `FileNotFoundError`: If test directory doesn't exist or config file specified but not found
- `NotADirectoryError`: If test_dir path is not a directory
- `ValueError`: If invalid browser, timeout, or workers value provided

### `run_web_tests_simple(test_dir)`

Simplified interface returning tuple.

**Returns:**
- Tuple of `(stdout, stderr, return_code)`

## Test File Requirements

Tests must use pytest-playwright:

```python
import pytest
from playwright.sync_api import Page, expect

def test_example(page: Page):
    page.goto("https://example.com")
    expect(page).to_have_title("Example Domain")
```

## Configuration

### Config File Format

Create `config/test_config.yaml` (or `test_config.yaml`) with the following structure:

```yaml
web:
  test_dir: "examples/web_tests"     # Required: Path to test directory
  browser: "chromium"                # Optional: chromium, firefox, or webkit
  headed: false                      # Optional: Show browser window
  workers: null                      # Optional: Number of parallel workers (null = sequential)
  verbose: true                      # Optional: Verbose pytest output
  timeout: 300                       # Optional: Execution timeout in seconds
```

**Config Search Paths:**

When `config_path` is not specified, the runner searches in order:
1. `config/test_config.yaml` (relative to current directory)
2. `test_config.yaml` (in current directory)

If no config file is found, built-in defaults are used.

**Config Validation:**

- `browser` must be one of: `chromium`, `firefox`, `webkit`
- `timeout` must be greater than 0
- `workers` must be >= 1 (or null for sequential execution)
- `test_dir` is validated for existence when tests are run

### Pytest Configuration

Create `conftest.py` in your test directory for pytest-specific configuration:

```python
import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
    }
```

## Examples

See `examples/web_tests/` for complete examples:
- `test_saucedemo.py` - Login flow tests
- `conftest.py` - Pytest configuration
- `run_web_tests.py` - Config-based runner usage
- `run_web_tests_with_overrides.py` - Config with parameter overrides

### Example 1: Using Config File

```python
from src.runners.web_runner import run_web_tests

# Uses default config search paths
result = run_web_tests()
print(f"Tests {'PASSED' if result.success else 'FAILED'}")
```

### Example 2: Custom Config Path

```python
from src.runners.web_runner import run_web_tests

result = run_web_tests(config_path="custom/path/config.yaml")
print(result.stdout)
```

### Example 3: Config + Overrides

```python
from src.runners.web_runner import run_web_tests

# Load from config but override browser and headed mode
result = run_web_tests(
    config_path="config/test_config.yaml",
    browser="firefox",
    headed=True
)
```

### Example 4: Direct Parameters (No Config)

```python
from src.runners.web_runner import run_web_tests

# All parameters specified directly
result = run_web_tests(
    test_dir="examples/web_tests",
    browser="webkit",
    headed=False,
    workers=4,
    verbose=True,
    timeout=600
)
```

## Return Codes

- `0` - All tests passed
- `1` - Tests failed
- `2` - Test execution was interrupted
- `3` - Internal error occurred
- `4` - pytest command line usage error
- `5` - No tests collected
- `124` - Execution timeout (300 seconds)
