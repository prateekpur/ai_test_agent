"""Example script with parameter overrides."""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from runners.web_runner import run_web_tests


def main():
    print("Running web tests with config + overrides...")
    print("=" * 60)

    result = run_web_tests(config_path="config/test_config.yaml", verbose=True, headed=False)

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
