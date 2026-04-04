from pathlib import Path

from src.agents.critic import analyze_test_results, print_analysis
from src.agents.generator import generate_web_tests
from src.agents.planner import plan_tests
from src.runners.web_runner import run_web_tests


def main():
    print("=" * 60)
    print("Phase 2 Critic - Example Usage")
    print("=" * 60)
    print()

    context = {"base_url": "https://www.saucedemo.com"}
    output_dir = "output/critic_test"
    
    print("Step 1: Create test plan")
    print("-" * 60)
    plan = plan_tests("test user login flow", context)
    print(f"Plan: {plan['test_name']}")
    print()

    print("Step 2: Generate test code")
    print("-" * 60)
    files = generate_web_tests(plan, output_dir)
    print(f"Generated: {files[0]}")
    print()

    print("Step 3: Run tests")
    print("-" * 60)
    result = run_web_tests(test_dir=output_dir, browser="chromium", headed=False)
    print(f"Return code: {result.return_code}")
    print()

    print("Step 4: Analyze results with Critic")
    print("-" * 60)
    analysis = analyze_test_results(result.stdout, result.stderr, result.return_code)
    
    print_analysis(analysis)
    
    print()
    print("Step 5: Programmatic access to analysis")
    print("-" * 60)
    print(f"Status: {analysis['status']}")
    print(f"Failure type: {analysis.get('failure_type', 'N/A')}")
    print(f"Failed tests: {len(analysis['failed_tests'])}")
    
    if analysis['failed_tests']:
        print("\nFirst failed test details:")
        first_fail = analysis['failed_tests'][0]
        print(f"  Name: {first_fail['name']}")
        print(f"  Error: {first_fail['error'][:100]}...")


if __name__ == "__main__":
    main()
