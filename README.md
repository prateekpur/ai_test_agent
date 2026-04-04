# AI Test Agent

Python-based AI-driven test automation system for Web tests with agent orchestration.

## Project Vision

This project aims to build an intelligent test automation platform that uses LLM agents to:
- Generate web test code from natural language descriptions
- Execute pytest-playwright tests for web applications
- Analyze failures and automatically fix issues
- Orchestrate complex testing workflows

See [PLAN.md](PLAN.md) for the complete roadmap.

## Current Status: Phase 2 Complete, Phase 3 Partial

✅ **Phase 0-2 Complete**: Full fake agent pipeline (Planner → Generator → Runner → Critic → Fixer)
✅ **Phase 3 Partial**: LLM-powered test generator CLI available

### Features

- 🤖 LLM-powered test generation from natural language descriptions
- 📝 Support for multiple test descriptions in a single file
- 🔧 GitHub Copilot API and OpenAI API compatible
- ✅ Generates clean, runnable pytest-playwright code
- 🎯 CLI tool for easy integration into workflows
- 🔄 Fake agent orchestration pipeline for validation

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r src/requirements.txt

# 2. Install development tools (optional)
pip install -r requirements-dev.txt

# 3. Set your API key
export GITHUB_TOKEN="your_github_token_here"
# OR
export OPENAI_API_KEY="your_openai_api_key_here"

# 4. Run the quick start guide
python quickstart.py

# 5. Generate tests from descriptions
python -m src.test_generator.cli \
  -i examples/test_descriptions.txt \
  -o output/test_generated.py
```

---

## Development

### Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linter and formatter
python lint.py

# Or use ruff directly
ruff check src/ examples/ --fix
ruff format src/ examples/
```

The linter runs:
- **Linting**: Checks for code quality issues (pycodestyle, pyflakes, etc.)
- **Formatting**: Auto-formats code to consistent style
- **Import sorting**: Organizes imports automatically

Configuration is in `pyproject.toml`.

---

## Test Generator Usage

### Input Format

Create a text file with your test descriptions:

```
## user login flow

Test that users can successfully log into the application.
Navigate to the login page and enter valid credentials.
Submit the form and verify successful authentication.

## search functionality

Test the search feature on the website.
Enter a search query in the search box.
Submit the search and verify results are displayed.
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
│   ├── agents/                 # ✅ Agent orchestration (Phase 2 - COMPLETED)
│   │   ├── planner.py          # Fake planner with 7 scenarios
│   │   ├── generator.py        # Template-based test generator
│   │   ├── critic.py           # Regex-based failure analyzer
│   │   └── fixer.py            # Log-based fix recommender
│   ├── runners/                # ✅ Test execution (Phase 1 - COMPLETED)
│   │   ├── web_runner.py       # pytest-playwright runner
│   │   └── config.py           # Configuration system
│   ├── test_generator/         # ✅ LLM test generator (Phase 3 - PARTIAL)
│   │   ├── cli.py              # CLI interface
│   │   ├── llm_client.py       # LLM API client
│   │   ├── parser.py           # Description file parser
│   │   ├── generator.py        # Test code generator
│   │   └── writer.py           # File writer
│   └── pages/                  # 🔜 Page objects (PLANNED - Phase 4)
├── examples/
│   ├── test_descriptions.txt   # Example input file
│   ├── planner_example.py      # Phase 2 examples
│   ├── generator_example.py
│   ├── critic_example.py
│   ├── fixer_example.py
│   └── e2e_pipeline.py         # Full pipeline demo
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

- [x] **Phase 0**: Project bootstrap and dependencies
- [x] **Phase 1**: Core web test runner infrastructure
- [x] **Phase 2**: Fake agent orchestration (Planner, Generator, Critic, Fixer)
- [ ] **Phase 3**: Real LLM integration (2/4 tasks complete)
- [ ] **Phase 4**: Advanced web features (page objects, visual regression)
- [ ] **Phase 5**: Workflow hardening (retry, reporting, parallel execution)
- [ ] **Phase 6**: Stretch goals (RAG, test memory, accessibility testing)

See [PLAN.md](PLAN.md) for detailed phase breakdown.

---

## Examples

See [examples/test_descriptions.txt](examples/test_descriptions.txt) for sample input format.

---

## License

MIT
