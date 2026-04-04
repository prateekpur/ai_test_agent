from src.agents.fixer import fix_tests


def test_passed_tests():
    print("Test 1: Passed tests (no fixes needed)")
    print("-" * 60)
    diagnosis = {
        "status": "passed",
        "total_tests": 3,
        "passed_tests": 3,
        "failed_tests": [],
        "duration": "2.34s",
    }
    fix_tests(diagnosis, ["test_example.py"])
    print()


def test_timeout_failure():
    print("Test 2: Timeout failure")
    print("-" * 60)
    diagnosis = {
        "status": "failed",
        "failure_type": "timeout",
        "total_tests": 1,
        "passed_tests": 0,
        "failed_tests": [
            {
                "file": "test_login.py",
                "name": "test_login_flow",
                "line": 15,
                "error": "Timeout 30000ms exceeded waiting for selector #submit-button",
            }
        ],
        "duration": "35.2s",
    }
    fix_tests(diagnosis, ["test_login.py"])
    print()


def test_locator_not_found():
    print("Test 3: Locator not found failure")
    print("-" * 60)
    diagnosis = {
        "status": "failed",
        "failure_type": "locator_not_found",
        "total_tests": 1,
        "passed_tests": 0,
        "failed_tests": [
            {
                "file": "test_search.py",
                "name": "test_search_functionality",
                "line": 22,
                "error": "Locator('#dynamic-search-box').click: Error: Element is not attached to the DOM",
            }
        ],
        "duration": "3.5s",
    }
    fix_tests(diagnosis, ["test_search.py"])
    print()


def test_assertion_failure():
    print("Test 4: Assertion failure")
    print("-" * 60)
    diagnosis = {
        "status": "failed",
        "failure_type": "assertion",
        "total_tests": 1,
        "passed_tests": 0,
        "failed_tests": [
            {
                "file": "test_checkout.py",
                "name": "test_checkout_process",
                "line": 45,
                "error": "AssertionError: Expected text 'Order Confirmed' but got 'Payment Pending'",
            }
        ],
        "duration": "8.1s",
    }
    fix_tests(diagnosis, ["test_checkout.py"])
    print()


def test_multiple_failures():
    print("Test 5: Multiple failures (same type)")
    print("-" * 60)
    diagnosis = {
        "status": "failed",
        "failure_type": "timeout",
        "total_tests": 3,
        "passed_tests": 0,
        "failed_tests": [
            {
                "file": "test_forms.py",
                "name": "test_form_submission",
                "line": 12,
                "error": "Timeout waiting for selector #first-name",
            },
            {
                "file": "test_forms.py",
                "name": "test_form_validation",
                "line": 28,
                "error": "Timeout waiting for selector .error-message",
            },
        ],
        "duration": "65.4s",
    }
    fix_tests(diagnosis, ["test_forms.py"])
    print()


def test_network_error():
    print("Test 6: Network error")
    print("-" * 60)
    diagnosis = {
        "status": "failed",
        "failure_type": "network",
        "total_tests": 1,
        "passed_tests": 0,
        "failed_tests": [
            {
                "file": "test_api.py",
                "name": "test_api_endpoint",
                "line": 8,
                "error": "net::ERR_CONNECTION_REFUSED at https://localhost:3000/api/users",
            }
        ],
        "duration": "1.2s",
    }
    fix_tests(diagnosis, ["test_api.py"])
    print()


def main():
    print("=" * 60)
    print("Fixer Unit Tests")
    print("=" * 60)
    print()

    test_passed_tests()
    test_timeout_failure()
    test_locator_not_found()
    test_assertion_failure()
    test_multiple_failures()
    test_network_error()

    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
