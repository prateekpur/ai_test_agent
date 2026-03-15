# AI Test Agent Project Plan

This plan covers the implementation of a Python-based AI-driven test automation system for API, Web, and Mobile tests with agent orchestration.

---

## Phase 0 – Project Bootstrap

- [ ] Create repo `ai_test_agent` and folder structure
- [ ] Create Python virtual environment
- [ ] Install dependencies: `pytest`, `requests`, `playwright`, `appium-python-client`
- [ ] Run `playwright install`
- [ ] Add `.env` for LLM keys
- [ ] Add `.gitignore`
- [ ] Verify `pytest` runs without errors

---

## Phase 1 – Core Infrastructure (No AI Yet)

- [ ] Implement API runner (`runners/api_runner.py`) with function `run_api_tests(test_dir)` returning stdout, stderr, return code
- [ ] Implement Web runner (`runners/web_runner.py`) with function `run_web_tests(test_dir)` returning stdout, stderr, return code
- [ ] Implement Mobile runner (`runners/mobile_runner.py`) with function `run_mobile_tests(test_dir)` returning stdout, stderr, return code
- [ ] Implement unified workflow skeleton (`workflows/unified_workflow.py`) with `run_test_task(type, description, base_url=None, app_caps=None)` to orchestrate runners

---

## Phase 2 – Fake Agents (No LLM Yet)

- [ ] Implement Fake Planner (`agents/planner.py`) with `plan_tests(type, description, context)` returning hard-coded plan
- [ ] Implement Generator for API tests (`agents/generator.py`) writing pytest files from plan
- [ ] Implement Critic (simple) (`agents/critic.py`) analyzing test run results and printing structured diagnosis
- [ ] Implement Fixer (dummy) (`agents/fixer.py`) logging which files would be fixed

---

## Phase 3 – Real LLM Integration (API Only)

- [ ] Implement common LLM client (`agents/llm_client.py`) with retries and timeout
- [ ] Real API Planner: prompt LLM to generate structured plan from goal and base URL
- [ ] Real API Generator: prompt LLM to produce pytest code and save deterministic files
- [ ] Real Critic: feed run results to LLM, classify failures (assertion, network, environment, bad test)
- [ ] Real Fixer: rewrite failing files based on critic diagnosis and re-run workflow

---

## Phase 4 – Web UI Tests

- [ ] Extend planner to generate web flows: page name + steps
- [ ] Implement Web Generator (`agents/generator.py`) to generate Playwright Python tests
- [ ] Improve Web Critic: classify failures like timeout, locator not found, assertion failures

---

## Phase 5 – Mobile / Device Tests

- [ ] Extend planner to generate mobile flows: screen + steps
- [ ] Implement Mobile Generator (`agents/generator.py`) to generate Appium Python tests
- [ ] Mobile Critic: classify failures like NoSuchElement, activity/screen mismatch, timeout

---

## Phase 6 – Workflow Hardening

- [ ] Add retry and recovery loop in workflow
- [ ] Save plan, generated files, run results, and critic diagnosis to `runs/<timestamp>/`
- [ ] Return unified structured report with status, iterations, failures, and files

---

## Phase 7 – Stretch Goals

- [ ] Implement RAG: feed OpenAPI docs, markdown, and PDFs to planner
- [ ] Implement test memory: store previous failures and flaky tests and feed to critic to improve future runs

---

# Notes

- **Agents:** only talk to LLM
- **Runners:** only execute code/tools
- **Workflow:** orchestrates everything
- Follow phases linearly for best results
