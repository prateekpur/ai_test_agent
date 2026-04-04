from pathlib import Path

from src.agents.generator import generate_multiple_tests, generate_web_tests
from src.agents.planner import plan_tests


def main():
    print("=" * 60)
    print("Phase 2 Generator - Example Usage")
    print("=" * 60)
    print()

    context = {"base_url": "https://www.saucedemo.com"}
    output_dir = "output/generated_tests"

    print("Example 1: Generate single test file")
    print("-" * 60)
    plan = plan_tests("test user login flow", context)
    print(f"Plan: {plan['test_name']} with {len(plan['steps'])} steps")

    files = generate_web_tests(plan, output_dir)
    print(f"Generated: {files[0]}")
    print()

    with Path(files[0]).open() as f:
        print("Generated code:")
        print(f.read())
    print()

    print("=" * 60)
    print("Example 2: Generate multiple tests in one file")
    print("-" * 60)

    descriptions = ["test user login flow", "test search functionality", "test navigation menu"]

    plans = [plan_tests(desc, context) for desc in descriptions]
    print(f"Created {len(plans)} test plans")

    files = generate_multiple_tests(plans, output_dir)
    print(f"Generated: {files[0]}")
    print()

    with Path(files[0]).open() as f:
        content = f.read()
        print(f"Generated code ({len(content)} chars, {content.count('def test_')} tests):")
        print(content[:500] + "..." if len(content) > 500 else content)


if __name__ == "__main__":
    main()
