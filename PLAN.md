# AI Test Agent Project Plan

This plan covers the implementation of a Python-based AI-driven test automation system for Web application tests with agent orchestration.

---

## Phase 0 – Project Bootstrap

- [x] Create repo `ai_test_agent` and folder structure
- [x] Create Python virtual environment
- [x] Install dependencies: `pytest`, `requests`, `playwright`
- [x] Run `playwright install`
- [x] Add `.env` for LLM keys
- [x] Add `.gitignore`
- [x] Verify `pytest` runs without errors

---

## Phase 1 – Core Infrastructure (No AI Yet)

- [x] Implement Web runner (`runners/web_runner.py`) with function `run_web_tests(test_dir)` returning stdout, stderr, return code

---

## Phase 2 – Fake Agents (No LLM Yet)

- [x] Implement Fake Planner (`agents/planner.py`) with `plan_tests(description, context)` returning hard-coded web test plan
- [x] Implement Generator for Web tests (`agents/generator.py`) writing pytest-playwright files from plan
- [ ] Implement Critic (simple) (`agents/critic.py`) analyzing test run results and printing structured diagnosis
- [ ] Implement Fixer (dummy) (`agents/fixer.py`) logging which files would be fixed

---

## Phase 3 – Real LLM Integration (Web Tests)

- [x] Implement common LLM client (`test_generator/llm_client.py`) with retries and timeout
- [ ] Real Web Planner: prompt LLM to generate structured test plan from description and base URL
- [x] Real Web Generator: prompt LLM to produce pytest-playwright code and save deterministic files
- [ ] Real Critic: feed run results to LLM, classify failures (timeout, locator not found, assertion, network, environment, bad test)
- [ ] Real Fixer: rewrite failing files based on critic diagnosis and re-run workflow

---

## Phase 4 – Advanced Web Test Features

- [ ] Extend planner to generate complex web flows: multi-page scenarios, form handling, navigation
- [ ] Implement page object model support in generator
- [ ] Add visual regression testing capabilities
- [ ] Improve Web Critic: detect flaky tests, suggest better locators, identify timing issues

---

## Phase 5 – Workflow Hardening

- [ ] Add retry and recovery loop for test execution
- [ ] Save plan, generated files, run results, and critic diagnosis to `runs/<timestamp>/`
- [ ] Return unified structured report with status, iterations, failures, and files
- [ ] Implement parallel test execution with sharding
- [ ] Add test result visualization and reporting

---

## Phase 6 – Stretch Goals

- [ ] Implement RAG: feed web app documentation, UI specs, and design docs to planner
- [ ] Implement test memory: store previous failures and flaky tests and feed to critic to improve future runs
- [ ] Add cross-browser testing orchestration (Chromium, Firefox, WebKit)
- [ ] Implement accessibility testing integration
- [ ] Add performance testing capabilities (Core Web Vitals)

---

# Notes

- **Agents:** only talk to LLM
- **Runners:** only execute code/tools
- Follow phases linearly for best results
