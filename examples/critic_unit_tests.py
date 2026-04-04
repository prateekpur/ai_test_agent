from src.agents.critic import analyze_test_results


def test_critic_with_passing_tests():
    print("\n" + "=" * 60)
    print("Test 1: Passing Tests")
    print("=" * 60)
    
    stdout = """
collected 3 items

test_example.py::test_login PASSED
test_example.py::test_search PASSED
test_example.py::test_logout PASSED

========================= 3 passed in 2.5s =========================
"""
    
    analysis = analyze_test_results(stdout, "", 0)
    
    assert analysis["status"] == "passed"
    assert analysis["passed"] == 3
    assert analysis["failed"] == 0
    assert analysis["failure_type"] is None
    assert len(analysis["failed_tests"]) == 0
    
    print("✓ Status:", analysis["status"])
    print("✓ Passed:", analysis["passed"])
    print("✓ Failed:", analysis["failed"])


def test_critic_with_timeout_failure():
    print("\n" + "=" * 60)
    print("Test 2: Timeout Failure")
    print("=" * 60)
    
    stdout = """collected 2 items

test_login.py::test_login_flow FAILED                                   [50%]
test_search.py::test_search PASSED                                      [100%]

================================= FAILURES =================================
_______________________________ test_login_flow ____________________________

page = <Page url='https://example.com/login'>

    def test_login_flow(page):
        page.goto("https://example.com/login")
>       page.click("#submit-button")
E       playwright._impl._api_types.TimeoutError: Timeout 30000ms exceeded.

test_login.py:8: TimeoutError

===================== short test summary info =====================
FAILED test_login.py::test_login_flow - playwright._impl._api_types.TimeoutError: Timeout 30000ms exceeded.
========================= 1 failed, 1 passed in 5.2s =========================
"""
    
    analysis = analyze_test_results(stdout, "", 1)
    
    assert analysis["status"] == "failed"
    assert analysis["passed"] == 1
    assert analysis["failed"] == 1
    assert analysis["failure_type"] == "timeout"
    assert len(analysis["failed_tests"]) == 1
    assert analysis["failed_tests"][0]["name"] == "test_login_flow"
    
    print("✓ Status:", analysis["status"])
    print("✓ Failure type:", analysis["failure_type"])
    print("✓ Failed test:", analysis["failed_tests"][0]["name"])
    print("✓ Diagnosis:", analysis["diagnosis"])
    print("✓ Suggested fix:", analysis["suggested_fix"])


def test_critic_with_assertion_failure():
    print("\n" + "=" * 60)
    print("Test 3: Assertion Failure")
    print("=" * 60)
    
    stdout = """collected 1 item

test_assertions.py::test_welcome_message FAILED                         [100%]

================================= FAILURES =================================
____________________________ test_welcome_message __________________________

page = <Page url='https://example.com/dashboard'>

    def test_welcome_message(page):
        page.goto("https://example.com/dashboard")
>       expect(page.locator(".welcome")).to_contain_text("Welcome Admin")
E       AssertionError: Expected "Welcome Admin" but received "Welcome User"

test_assertions.py:12: AssertionError

===================== short test summary info =====================
FAILED test_assertions.py::test_welcome_message - AssertionError: Expected "Welcome Admin" but received "Welcome User"
========================= 1 failed in 1.5s =========================
"""
    
    analysis = analyze_test_results(stdout, "", 1)
    
    assert analysis["status"] == "failed"
    assert analysis["failed"] == 1
    assert analysis["failure_type"] == "assertion"
    assert "Welcome Admin" in analysis["failed_tests"][0]["error"]
    
    print("✓ Status:", analysis["status"])
    print("✓ Failure type:", analysis["failure_type"])
    print("✓ Error:", analysis["failed_tests"][0]["error"][:80])


def test_critic_with_locator_not_found():
    print("\n" + "=" * 60)
    print("Test 4: Locator Not Found")
    print("=" * 60)
    
    stdout = """collected 1 item

test_selectors.py::test_click_button FAILED                             [100%]

================================= FAILURES =================================
_____________________________ test_click_button ____________________________

    def test_click_button(page):
        page.goto("https://example.com")
>       page.click("#non-existent-button")
E       Error: locator.click: Target closed

test_selectors.py:5: Error

===================== short test summary info =====================
FAILED test_selectors.py::test_click_button - Error: locator.click: Target closed
========================= 1 failed in 0.8s =========================
"""
    
    analysis = analyze_test_results(stdout, "", 1)
    
    assert analysis["status"] == "failed"
    assert analysis["failure_type"] == "locator_not_found"
    
    print("✓ Status:", analysis["status"])
    print("✓ Failure type:", analysis["failure_type"])
    print("✓ Suggested fix:", analysis["suggested_fix"])


def run_all_tests():
    print("=" * 60)
    print("Running Critic Unit Tests")
    print("=" * 60)
    
    test_critic_with_passing_tests()
    test_critic_with_timeout_failure()
    test_critic_with_assertion_failure()
    test_critic_with_locator_not_found()
    
    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
