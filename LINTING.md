# Linting and Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) - an extremely fast Python linter and code formatter written in Rust.

## Why Ruff?

- **Fast**: 10-100x faster than traditional tools (Black, Flake8, isort)
- **All-in-one**: Replaces multiple tools with a single dependency
- **Compatible**: Drop-in replacement for Flake8, isort, Black, and more
- **Modern**: Includes latest Python best practices and rules

## Installation

```bash
pip install -r requirements-dev.txt
```

## Usage

### Quick Run

```bash
python lint.py
```

This runs both linting and formatting with auto-fix enabled.

### Manual Commands

```bash
ruff check src/ examples/ --fix
ruff format src/ examples/
```

### Check Only (No Auto-Fix)

```bash
ruff check src/ examples/
```

## Configuration

Linter configuration is in `pyproject.toml`:

### Enabled Rules

- **E/W**: pycodestyle errors and warnings
- **F**: pyflakes (unused imports, undefined names)
- **I**: isort (import sorting)
- **N**: pep8-naming (naming conventions)
- **UP**: pyupgrade (modern Python syntax)
- **B**: flake8-bugbear (common bugs)
- **C4**: flake8-comprehensions (better comprehensions)
- **SIM**: flake8-simplify (code simplification)
- **PIE**: flake8-pie (miscellaneous improvements)
- **RET**: flake8-return (return statement issues)
- **RSE**: flake8-raise (exception raising issues)
- **PTH**: flake8-use-pathlib (prefer pathlib over os.path)

### Project Settings

- **Line length**: 100 characters
- **Target Python**: 3.8+
- **Quote style**: Double quotes
- **Import sorting**: Automatic with known first-party packages

### Per-File Ignores

- `__init__.py`: Allows unused imports (F401)
- `examples/*.py`: Allows print statements (T201) and module imports not at top (E402)
- `tests/*.py`: Allows non-lowercase names (N802, N803)

## What Gets Checked

### Linting

- Code style (PEP 8)
- Unused imports and variables
- Undefined names
- Import order
- Naming conventions
- Common bug patterns
- Code complexity

### Formatting

- Consistent indentation (4 spaces)
- Quote normalization (double quotes)
- Line length enforcement (100 chars)
- Trailing whitespace removal
- Blank line consistency

## CI Integration

Add to your CI pipeline:

```yaml
- name: Lint with Ruff
  run: |
    pip install -r requirements-dev.txt
    ruff check src/ examples/
    ruff format --check src/ examples/
```

## Pre-commit Hook (Optional)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
python lint.py
if [ $? -ne 0 ]; then
    echo "Linting failed. Please fix errors before committing."
    exit 1
fi
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

## IDE Integration

### VS Code

Install the Ruff extension:
```
ext install charliermarsh.ruff
```

Add to `.vscode/settings.json`:
```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true
  }
}
```

### PyCharm

1. Go to Settings → Tools → External Tools
2. Add new tool:
   - Name: Ruff
   - Program: ruff
   - Arguments: check --fix $FilePath$
   - Working directory: $ProjectFileDir$

## Troubleshooting

### Import Errors

If you see `E402` (module level import not at top), it's usually intentional in example scripts. Add to per-file-ignores in `pyproject.toml`.

### Line Too Long

Ruff formatter handles most cases automatically. For edge cases:
- Split long strings across multiple lines
- Use parentheses for line continuation
- Refactor complex expressions

### False Positives

To ignore a specific line:
```python
result = some_function()  # noqa: RET504
```

To ignore a rule globally, add to `ignore` list in `pyproject.toml`.

## Reference

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Rule Reference](https://docs.astral.sh/ruff/rules/)
- [Configuration](https://docs.astral.sh/ruff/configuration/)
