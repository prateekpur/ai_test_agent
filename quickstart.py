#!/usr/bin/env python3
import os
import sys

def check_api_key():
    github_token = os.getenv('GITHUB_TOKEN')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if not github_token and not openai_key:
        print("⚠️  Warning: No API key found!")
        print("\nSet one of the following environment variables:")
        print("  export GITHUB_TOKEN='your_github_token'")
        print("  export OPENAI_API_KEY='your_openai_key'")
        return False
    
    if github_token:
        print("✓ GITHUB_TOKEN found")
    if openai_key:
        print("✓ OPENAI_API_KEY found")
    
    return True

def main():
    print("=" * 60)
    print("Test Generator CLI - Quick Start")
    print("=" * 60)
    print()
    
    check_api_key()
    
    print("\nExample usage:")
    print()
    print("  # Basic usage")
    print("  python -m src.test_generator.cli \\")
    print("    -i examples/test_descriptions.txt \\")
    print("    -o output/test_generated.py")
    print()
    print("  # With specific model")
    print("  python -m src.test_generator.cli \\")
    print("    -i examples/test_descriptions.txt \\")
    print("    -o output/test_generated.py \\")
    print("    --model gpt-4o")
    print()
    print("Example description file format:")
    print("-" * 60)
    print("""## user authentication

Test that login validates credentials correctly.
Should accept valid username/password.
Should reject invalid credentials.

## password validation

Test password strength requirements.
Must have 8+ chars, uppercase, and number.""")
    print("-" * 60)
    print()
    print("For more details, see: src/test_generator/README.md")
    print()

if __name__ == '__main__':
    main()
