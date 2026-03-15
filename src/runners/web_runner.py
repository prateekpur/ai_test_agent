import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

from .config import load_config


@dataclass
class TestResult:
    stdout: str
    stderr: str
    return_code: int

    @property
    def success(self) -> bool:
        return self.return_code == 0

    @property
    def failed(self) -> bool:
        return self.return_code != 0


def run_web_tests(
    test_dir: Optional[str] = None,
    browser: Optional[str] = None,
    headed: Optional[bool] = None,
    workers: Optional[int] = None,
    verbose: Optional[bool] = None,
    config_path: Optional[str] = None,
) -> TestResult:
    config = load_config(config_path)
    web_config = config.web

    final_test_dir = test_dir if test_dir is not None else web_config.test_dir
    final_browser = browser if browser is not None else web_config.browser
    final_headed = headed if headed is not None else web_config.headed
    final_workers = workers if workers is not None else web_config.workers
    final_verbose = verbose if verbose is not None else web_config.verbose
    final_timeout = web_config.timeout

    test_path = Path(final_test_dir)

    if not test_path.exists():
        raise FileNotFoundError(f"Test directory not found: {final_test_dir}")

    if not test_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {final_test_dir}")

    pytest_args = [
        sys.executable,
        "-m",
        "pytest",
        str(test_path),
        "--browser",
        final_browser,
    ]

    if final_headed:
        pytest_args.append("--headed")

    if final_workers:
        pytest_args.extend(["-n", str(final_workers)])

    if final_verbose:
        pytest_args.append("-v")

    pytest_args.extend(["--tb=short", "--color=yes"])

    try:
        result = subprocess.run(pytest_args, capture_output=True, text=True, timeout=final_timeout)

        return TestResult(stdout=result.stdout, stderr=result.stderr, return_code=result.returncode)

    except subprocess.TimeoutExpired:
        return TestResult(
            stdout="",
            stderr=f"Test execution timed out after {final_timeout} seconds",
            return_code=124,
        )

    except Exception as e:
        return TestResult(stdout="", stderr=f"Test execution failed: {str(e)}", return_code=1)


def run_web_tests_simple(
    test_dir: Optional[str] = None, config_path: Optional[str] = None
) -> Tuple[str, str, int]:
    result = run_web_tests(test_dir=test_dir, config_path=config_path)
    return result.stdout, result.stderr, result.return_code
