from pathlib import Path

from src.agents.generator import generate_web_tests
from src.agents.planner import plan_tests


def test_planner_to_generator_integration():
    print("Testing Planner → Generator → Runner Integration")
    print("=" * 60)

    context = {"base_url": "https://www.saucedemo.com"}
    output_dir = "output/integration_test"

    test_scenarios = [
        "test user login flow",
        "test search functionality",
        "test checkout process",
    ]

    for description in test_scenarios:
        print(f"\n{description}")
        print("-" * 60)

        plan = plan_tests(description, context)
        print(f"✓ Plan created: {plan['test_name']}")
        print(f"  Steps: {len(plan['steps'])}")

        files = generate_web_tests(plan, output_dir)
        print(f"✓ Generated: {Path(files[0]).name}")

        with Path(files[0]).open() as f:
            code = f.read()
            print(f"  Lines of code: {len(code.splitlines())}")
            print(f"  Contains 'def {plan['test_name']}': {plan['test_name'] in code}")

    print("\n" + "=" * 60)
    print("✓ Integration test complete")
    print(f"Generated files in: {output_dir}/")


if __name__ == "__main__":
    test_planner_to_generator_integration()
