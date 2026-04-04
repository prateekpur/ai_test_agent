"""Example usage of Phase 2 Fake Planner."""

from src.agents.planner import get_supported_scenarios, plan_tests


def main():
    print("=" * 60)
    print("Phase 2 Fake Planner - Example Usage")
    print("=" * 60)
    print()

    context = {"base_url": "https://example.com", "browser": "chromium"}

    print("Supported scenarios:")
    for scenario in get_supported_scenarios():
        print(f"  - {scenario}")
    print()

    test_descriptions = [
        "test user login flow",
        "test search functionality",
        "test checkout process",
        "test contact form submission",
        "test user registration",
        "test navigation menu",
        "test generic page load",
    ]

    for description in test_descriptions:
        print(f"\nDescription: '{description}'")
        print("-" * 60)
        plan = plan_tests(description, context)
        print(f"Test name: {plan['test_name']}")
        print(f"Steps: {len(plan['steps'])}")
        for i, step in enumerate(plan["steps"], 1):
            print(f"  {i}. {step['action']}: {step['description']}")
        print()


if __name__ == "__main__":
    main()
