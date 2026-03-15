"""Example script demonstrating web runner usage."""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from runners.web_runner import run_web_tests


def main():
    print("Running web tests with configuration...")
    print("=" * 60)

    # Ensure we're running from project root for relative paths to work
    config_path = project_root / "config" / "test_config.yaml"

    result = run_web_tests(config_path=str(config_path))

    print("\nSTDOUT:")
    print(result.stdout)

    if result.stderr:
        print("\nSTDERR:")
        print(result.stderr)

    print("\n" + "=" * 60)
    print(f"Return Code: {result.return_code}")
    print(f"Status: {'✓ PASSED' if result.success else '✗ FAILED'}")

    return result.return_code


if __name__ == "__main__":
    sys.exit(main())
