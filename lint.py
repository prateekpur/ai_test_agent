#!/usr/bin/env python
"""Run linting and formatting checks on the codebase."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> int:
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    project_root = Path(__file__).parent
    
    commands = [
        (
            ["ruff", "check", "src/", "examples/", "--fix"],
            "Running Ruff linter (auto-fix enabled)"
        ),
        (
            ["ruff", "format", "src/", "examples/"],
            "Running Ruff formatter"
        ),
    ]
    
    exit_code = 0
    for cmd, description in commands:
        result = run_command(cmd, description)
        if result != 0:
            exit_code = result
    
    if exit_code == 0:
        print(f"\n{'='*60}")
        print("✓ All checks passed!")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'='*60}")
        print("✗ Some checks failed")
        print(f"{'='*60}\n")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
