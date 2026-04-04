from pathlib import Path

from src.agents.critic import analyze_test_results
from src.agents.fixer import fix_tests
from src.agents.generator import generate_web_tests
from src.agents.planner import plan_tests
from src.runners.web_runner import run_web_tests


def main():
    print("=" * 60)
    print("Phase 2 Fixer - Example Usage")
    print("=" * 60)
    print()

    context = {"base_url": "https://www.saucedemo.com"}
    output_dir = "output/fixer_test"
    
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
    diagnosis = analyze_test_results(result.stdout, result.stderr, result.return_code)
    print(f"Status: {diagnosis['status']}")
    print(f"Failure type: {diagnosis.get('failure_type', 'N/A')}")
    print()

    print("Step 5: Get fix recommendations from Fixer")
    print("-" * 60)
    fix_tests(diagnosis, files)


if __name__ == "__main__":
    main()
