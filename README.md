# AI Test Agent

Python-based AI-driven test automation system for API, Web, and Mobile tests with agent orchestration.

## Project Vision

This project aims to build an intelligent test automation platform that uses LLM agents to:
- Generate test code from natural language descriptions
- Execute tests across multiple platforms (API, Web, Mobile)
- Analyze failures and automatically fix issues
- Orchestrate complex testing workflows

See [PLAN.md](PLAN.md) for the complete roadmap.

## Current Status: Test Generator (Phase 3 - Partial)

✅ **Available Now**: CLI tool to generate pytest tests from text descriptions using LLM

### Features

- 🤖 LLM-powered test generation from natural language descriptions
- 📝 Support for multiple test descriptions in a single file
- 🔧 GitHub Copilot API and OpenAI API compatible
- ✅ Generates clean, runnable pytest code
- 🎯 CLI tool for easy integration into workflows

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r src/requirements.txt

# 2. Set your API key
export GITHUB_TOKEN="your_github_token_here"
# OR
export OPENAI_API_KEY="your_openai_api_key_here"

# 3. Run the quick start guide
python quickstart.py

# 4. Generate tests from descriptions
python -m src.test_generator.cli \
  -i examples/test_descriptions.txt \
  -o output/test_generated.py
```

---

## Test Generator Usage

### Input Format

Create a text file with your test descriptions:

```
## user login validation

Test that user login works correctly with valid credentials.
Should reject invalid usernames and passwords.

## password strength checker

Test password strength validation function.
Passwords must have at least 8 characters, one uppercase, one number.
```

### Generate Tests

```bash
python -m src.test_generator.cli -i descriptions.txt -o test_output.py
```

### CLI Options

```
-i, --input       Input file with test descriptions (required)
-o, --output      Output file for generated pytest tests (required)
--model           LLM model to use (default: gpt-4o-mini)
--api-base        Custom API base URL (optional)
```

---

## Project Structure

```
ai_test_agent/
├── src/
│   ├── test_generator/         # ✅ LLM test code generator (COMPLETED)
│   │   ├── cli.py              # CLI interface
│   │   ├── llm_client.py       # LLM API client
│   │   ├── parser.py           # Description file parser
│   │   ├── generator.py        # Test code generator
│   │   └── writer.py           # File writer
│   ├── engine/                 # 🔜 Test execution engine (PLANNED)
│   ├── pages/                  # 🔜 Page objects (PLANNED)
│   └── tests/                  # 🔜 Generated tests (PLANNED)
├── examples/
│   └── test_descriptions.txt   # Example input file
├── PLAN.md                     # Full project roadmap
├── quickstart.py               # Quick start guide
└── README.md                   # This file
```

---

## Authentication

The test generator supports two authentication methods:

1. **GitHub Token** (for GitHub Copilot API)
   - Create a Personal Access Token with `models:read` permission
   - Set as `GITHUB_TOKEN` environment variable

2. **OpenAI API Key**
   - Get your API key from OpenAI
   - Set as `OPENAI_API_KEY` environment variable

---

## Documentation

- [PLAN.md](PLAN.md) - Complete project roadmap
- [Example Descriptions](examples/test_descriptions.txt) - Sample input file
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md) - Technical details

---

## Roadmap

- [x] **Phase 3 (Partial)**: LLM-based test generator with GitHub Copilot/OpenAI integration
- [ ] **Phase 1**: Core test runners (API, Web, Mobile)
- [ ] **Phase 2**: Agent orchestration (Planner, Critic, Fixer)
- [ ] **Phase 3 (Complete)**: Full LLM integration with self-healing tests
- [ ] **Phase 4-7**: Advanced features (Web UI, Mobile, RAG, Test Memory)

See [PLAN.md](PLAN.md) for detailed phase breakdown.

---

## Examples

See [examples/test_descriptions.txt](examples/test_descriptions.txt) for sample input format.

---

## License

MIT
