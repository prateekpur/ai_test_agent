"""
Fake Planner - Phase 2 Implementation

Returns hard-coded test plans based on keyword matching.
No LLM integration - validates architecture before adding AI complexity.
"""

from typing import Any, Dict, List


def plan_tests(description: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate hard-coded web test plan (no LLM).

    Args:
        description: Test description (e.g., "test user login flow")
        context: Additional context with keys:
            - base_url: Base URL of the web application
            - viewport: Optional viewport size (default: 1280x720)
            - browser: Optional browser (default: chromium)

    Returns:
        Test plan structure:
        {
            "test_name": str,
            "description": str,
            "steps": [
                {
                    "action": str,  # navigate, fill, click, assert_visible, assert_text
                    "selector": str (optional),
                    "url": str (optional),
                    "value": str (optional),
                    "expected": str (optional),
                    "contains": str (optional),
                    "description": str
                }
            ],
            "setup": {
                "viewport": {"width": int, "height": int},
                "browser": str
            }
        }

    Example:
        >>> plan = plan_tests("test login", {"base_url": "https://example.com"})
        >>> plan["test_name"]
        'test_login_flow'
        >>> len(plan["steps"])
        5
    """
    desc_lower = description.lower()
    base_url = context.get("base_url", "https://example.com")
    viewport = context.get("viewport", {"width": 1280, "height": 720})
    browser = context.get("browser", "chromium")

    setup = {"viewport": viewport, "browser": browser}

    # Login flow
    if "login" in desc_lower:
        return {
            "test_name": "test_login_flow",
            "description": description,
            "steps": [
                {
                    "action": "navigate",
                    "url": f"{base_url}/login",
                    "description": "Navigate to login page",
                },
                {
                    "action": "fill",
                    "selector": "#username",
                    "value": "testuser@example.com",
                    "description": "Enter username",
                },
                {
                    "action": "fill",
                    "selector": "#password",
                    "value": "password123",
                    "description": "Enter password",
                },
                {
                    "action": "click",
                    "selector": "button[type='submit']",
                    "description": "Click login button",
                },
                {
                    "action": "assert_visible",
                    "selector": ".user-profile, .dashboard, [data-testid='user-menu']",
                    "description": "Verify user is logged in",
                },
            ],
            "setup": setup,
        }

    # Search functionality
    elif "search" in desc_lower:
        return {
            "test_name": "test_search_functionality",
            "description": description,
            "steps": [
                {
                    "action": "navigate",
                    "url": base_url,
                    "description": "Navigate to home page",
                },
                {
                    "action": "fill",
                    "selector": "#search, input[type='search'], [data-testid='search-input']",
                    "value": "playwright",
                    "description": "Enter search term",
                },
                {
                    "action": "click",
                    "selector": "#search-button, button[type='submit'], [data-testid='search-button']",
                    "description": "Click search button",
                },
                {
                    "action": "assert_visible",
                    "selector": ".search-results, [data-testid='search-results']",
                    "description": "Verify search results are displayed",
                },
                {
                    "action": "assert_text",
                    "selector": ".results-count, [data-testid='results-count']",
                    "contains": "result",
                    "description": "Verify results count is shown",
                },
            ],
            "setup": setup,
        }

    # Checkout/purchase flow
    elif "checkout" in desc_lower or "purchase" in desc_lower or "cart" in desc_lower:
        return {
            "test_name": "test_checkout_process",
            "description": description,
            "steps": [
                {
                    "action": "navigate",
                    "url": f"{base_url}/cart",
                    "description": "Navigate to shopping cart",
                },
                {
                    "action": "click",
                    "selector": ".checkout-button, [data-testid='checkout-button']",
                    "description": "Click checkout button",
                },
                {
                    "action": "fill",
                    "selector": "#email, [name='email']",
                    "value": "customer@example.com",
                    "description": "Enter email address",
                },
                {
                    "action": "fill",
                    "selector": "#card-number, [name='cardnumber']",
                    "value": "4111111111111111",
                    "description": "Enter credit card number",
                },
                {
                    "action": "click",
                    "selector": "#submit-order, [data-testid='submit-order']",
                    "description": "Submit order",
                },
                {
                    "action": "assert_visible",
                    "selector": ".order-confirmation, [data-testid='order-confirmation']",
                    "description": "Verify order confirmation is shown",
                },
            ],
            "setup": setup,
        }

    # Form submission
    elif "form" in desc_lower or "submit" in desc_lower or "contact" in desc_lower:
        return {
            "test_name": "test_form_submission",
            "description": description,
            "steps": [
                {
                    "action": "navigate",
                    "url": f"{base_url}/contact",
                    "description": "Navigate to contact form",
                },
                {
                    "action": "fill",
                    "selector": "#name, [name='name']",
                    "value": "John Doe",
                    "description": "Enter name",
                },
                {
                    "action": "fill",
                    "selector": "#email, [name='email']",
                    "value": "john@example.com",
                    "description": "Enter email",
                },
                {
                    "action": "fill",
                    "selector": "#message, [name='message'], textarea",
                    "value": "This is a test message",
                    "description": "Enter message",
                },
                {
                    "action": "click",
                    "selector": "button[type='submit'], .submit-button",
                    "description": "Submit form",
                },
                {
                    "action": "assert_visible",
                    "selector": ".success-message, [data-testid='success-message']",
                    "description": "Verify success message is shown",
                },
            ],
            "setup": setup,
        }

    # Registration/signup
    elif "register" in desc_lower or "signup" in desc_lower or "sign up" in desc_lower:
        return {
            "test_name": "test_user_registration",
            "description": description,
            "steps": [
                {
                    "action": "navigate",
                    "url": f"{base_url}/signup",
                    "description": "Navigate to signup page",
                },
                {
                    "action": "fill",
                    "selector": "#username, [name='username']",
                    "value": "newuser",
                    "description": "Enter username",
                },
                {
                    "action": "fill",
                    "selector": "#email, [name='email']",
                    "value": "newuser@example.com",
                    "description": "Enter email",
                },
                {
                    "action": "fill",
                    "selector": "#password, [name='password']",
                    "value": "SecurePass123!",
                    "description": "Enter password",
                },
                {
                    "action": "fill",
                    "selector": "#confirm-password, [name='confirmPassword']",
                    "value": "SecurePass123!",
                    "description": "Confirm password",
                },
                {
                    "action": "click",
                    "selector": "button[type='submit'], .signup-button",
                    "description": "Submit registration",
                },
                {
                    "action": "assert_visible",
                    "selector": ".welcome-message, [data-testid='welcome']",
                    "description": "Verify welcome message is shown",
                },
            ],
            "setup": setup,
        }

    # Navigation test
    elif "navigation" in desc_lower or "menu" in desc_lower:
        return {
            "test_name": "test_navigation",
            "description": description,
            "steps": [
                {
                    "action": "navigate",
                    "url": base_url,
                    "description": "Navigate to home page",
                },
                {
                    "action": "click",
                    "selector": ".menu-button, [data-testid='menu-button']",
                    "description": "Open navigation menu",
                },
                {
                    "action": "assert_visible",
                    "selector": ".menu-items, nav",
                    "description": "Verify menu is visible",
                },
                {
                    "action": "click",
                    "selector": "a[href='/about'], .about-link",
                    "description": "Click about link",
                },
                {
                    "action": "assert_text",
                    "selector": "h1",
                    "contains": "About",
                    "description": "Verify about page heading",
                },
            ],
            "setup": setup,
        }

    # Default generic test plan
    else:
        return {
            "test_name": "test_generic_flow",
            "description": description,
            "steps": [
                {
                    "action": "navigate",
                    "url": base_url,
                    "description": "Navigate to home page",
                },
                {
                    "action": "assert_visible",
                    "selector": "body",
                    "description": "Verify page loaded successfully",
                },
                {
                    "action": "assert_text",
                    "selector": "h1, .page-title",
                    "contains": "",
                    "description": "Verify page has a heading",
                },
            ],
            "setup": setup,
        }


def get_supported_scenarios() -> List[str]:
    """
    Return list of supported test scenarios.

    Returns:
        List of scenario keywords that have hard-coded plans
    """
    return [
        "login",
        "search",
        "checkout",
        "purchase",
        "cart",
        "form",
        "submit",
        "contact",
        "register",
        "signup",
        "navigation",
        "menu",
    ]
