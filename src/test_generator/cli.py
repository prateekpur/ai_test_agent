import argparse
import sys
from pathlib import Path
from .llm_client import LLMClient
from .generator import TestGenerator


def main():
    parser = argparse.ArgumentParser(
        description='Generate pytest tests from text descriptions using LLM'
    )
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Input file containing test descriptions'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output file for generated pytest tests'
    )
    
    parser.add_argument(
        '--model',
        default='gpt-4o-mini',
        help='LLM model to use (default: gpt-4o-mini)'
    )
    
    parser.add_argument(
        '--api-base',
        help='Custom API base URL (default: OpenAI or GITHUB_TOKEN endpoint)'
    )
    
    args = parser.parse_args()
    
    try:
        llm_client = LLMClient(
            api_base=args.api_base,
            model=args.model
        )
        
        generator = TestGenerator(llm_client)
        
        print(f"Reading descriptions from: {args.input}")
        print(f"Generating tests using model: {args.model}")
        
        generator.generate_from_file(args.input, args.output)
        
        print(f"✓ Tests generated successfully: {args.output}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
