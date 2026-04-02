from pathlib import Path
from typing import Any, Dict, List


class ActionTemplate:
    NAVIGATE = '    page.goto("{url}")'
    FILL = '    page.fill("{selector}", "{value}")'
    CLICK = '    page.click("{selector}")'
    ASSERT_VISIBLE = '    expect(page.locator("{selector}")).to_be_visible()'
    ASSERT_TEXT = '    expect(page.locator("{selector}")).to_contain_text("{contains}")'


IMPORTS = """from playwright.sync_api import Page, expect


"""

TEST_FUNCTION_TEMPLATE = """def {test_name}(page: Page):
{body}
"""


def _generate_step_code(step: Dict[str, Any]) -> str:
    action = step["action"]
    
    if action == "navigate":
        return ActionTemplate.NAVIGATE.format(url=step["url"])
    elif action == "fill":
        return ActionTemplate.FILL.format(
            selector=step["selector"],
            value=step["value"]
        )
    elif action == "click":
        return ActionTemplate.CLICK.format(selector=step["selector"])
    elif action == "assert_visible":
        return ActionTemplate.ASSERT_VISIBLE.format(selector=step["selector"])
    elif action == "assert_text":
        return ActionTemplate.ASSERT_TEXT.format(
            selector=step["selector"],
            contains=step.get("contains", "")
        )
    else:
        raise ValueError(f"Unknown action type: {action}")


def generate_test_code(plan: Dict[str, Any]) -> str:
    steps_code = []
    
    for step in plan["steps"]:
        try:
            step_code = _generate_step_code(step)
            steps_code.append(step_code)
        except KeyError as e:
            raise ValueError(f"Missing required field in step: {e}. Step: {step}")
    
    body = "\n".join(steps_code)
    
    test_code = TEST_FUNCTION_TEMPLATE.format(
        test_name=plan["test_name"],
        body=body
    )
    
    return IMPORTS + test_code


def generate_web_tests(plan: Dict[str, Any], output_dir: str) -> List[str]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    test_code = generate_test_code(plan)
    
    test_filename = f"{plan['test_name']}.py"
    filepath = output_path / test_filename
    
    with filepath.open("w") as f:
        f.write(test_code)
    
    return [str(filepath)]


def generate_multiple_tests(plans: List[Dict[str, Any]], output_dir: str) -> List[str]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    all_test_code = [IMPORTS.strip()]
    
    for plan in plans:
        steps_code = []
        for step in plan["steps"]:
            step_code = _generate_step_code(step)
            steps_code.append(step_code)
        
        body = "\n".join(steps_code)
        test_func = TEST_FUNCTION_TEMPLATE.format(
            test_name=plan["test_name"],
            body=body
        )
        all_test_code.append(test_func.strip())
    
    combined_filename = "test_generated.py"
    filepath = output_path / combined_filename
    
    with filepath.open("w") as f:
        f.write("\n\n\n".join(all_test_code))
    
    return [str(filepath)]
