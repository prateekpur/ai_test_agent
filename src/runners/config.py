from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


@dataclass
class WebTestConfig:
    test_dir: str
    browser: str = "chromium"
    headed: bool = False
    workers: Optional[int] = None
    verbose: bool = False
    timeout: int = 300

    def validate(self) -> None:
        if self.browser not in ["chromium", "firefox", "webkit"]:
            raise ValueError(
                f"Invalid browser: {self.browser}. Must be chromium, firefox, or webkit"
            )

        if self.timeout <= 0:
            raise ValueError(f"Invalid timeout: {self.timeout}. Must be positive")

        if self.workers is not None and self.workers < 1:
            raise ValueError(f"Invalid workers: {self.workers}. Must be >= 1 or None")


@dataclass
class TestConfig:
    web: WebTestConfig

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TestConfig":
        web_data = data.get("web", {})
        web_config = WebTestConfig(**web_data)
        web_config.validate()
        return cls(web=web_config)

    @classmethod
    def from_yaml(cls, config_path: str) -> "TestConfig":
        path = Path(config_path)

        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with path.open() as f:
            data = yaml.safe_load(f)

        return cls.from_dict(data)

    @classmethod
    def default(cls) -> "TestConfig":
        return cls(web=WebTestConfig(test_dir="examples/web_tests"))


def load_config(config_path: Optional[str] = None) -> TestConfig:
    if config_path is None:
        default_paths = ["config/test_config.yaml", "test_config.yaml", ".test_config.yaml"]

        for path in default_paths:
            if Path(path).exists():
                config_path = path
                break

    if config_path and Path(config_path).exists():
        return TestConfig.from_yaml(config_path)

    return TestConfig.default()
