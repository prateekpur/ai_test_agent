from pathlib import Path

from src.agents.critic import analyze_test_results, print_analysis
from src.agents.generator import generate_web_tests
from src.agents.planner import plan_tests
from src.runners.web_runner import run_web_tests


def main():
    print("=" * 60)
    print("End-to-End Phase 2 Pipeline")
    print("Planner → Generator → Runner → Critic")
    print("=" * 60)
    print()

    context = {"base_url": "https://www.saucedemo.com"}
    output_dir = "output/e2e_test"
    
    test_descriptions = [
        "test user login flow",
        "test search functionality",
    ]
    
    for i, description in enumerate(test_descriptions, 1):
        print(f"\n{'=' * 60}")
        print(f"Test Scenario {i}: {description}")
        print(f"{'=' * 60}\n")
        
        print(f"[1/4] Planning...")
        plan = plan_tests(description, context)
        print(f"      ✓ Created plan: {plan['test_name']}")
        print(f"      ✓ Steps: {len(plan['steps'])}")
        
        print(f"\n[2/4] Generating test code...")
        files = generate_web_tests(plan, output_dir)
        print(f"      ✓ Generated: {Path(files[0]).name}")
        
        print(f"\n[3/4] Running tests...")
        result = run_web_tests(
            test_dir=output_dir,
            browser="chromium",
            headed=False,
            verbose=False
        )
        print(f"      ✓ Executed (exit code: {result.return_code})")
        
        print(f"\n[4/4] Analyzing results with Critic...")
        analysis = analyze_test_results(result.stdout, result.stderr, result.return_code)
        
        print()
        print_analysis(analysis)
        
        Path(files[0]).unlink()
    
    print(f"\n{'=' * 60}")
    print("✓ End-to-End Pipeline Complete")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
