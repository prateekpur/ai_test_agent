from pathlib import Path
from typing import Dict, List


class DescriptionParser:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Description file not found: {file_path}")

    def parse(self) -> List[Dict[str, str]]:
        with self.file_path.open(encoding="utf-8") as f:
            content = f.read()

        descriptions = []
        current_description = []
        current_name = None

        for line in content.splitlines():
            line = line.rstrip()

            if line.startswith("## "):
                if current_description:
                    descriptions.append(
                        {
                            "name": current_name or f"test_{len(descriptions) + 1}",
                            "description": "\n".join(current_description).strip(),
                        }
                    )
                current_name = line[3:].strip().replace(" ", "_").lower()
                current_description = []
            elif line.strip():
                current_description.append(line)

        if current_description:
            descriptions.append(
                {
                    "name": current_name or f"test_{len(descriptions) + 1}",
                    "description": "\n".join(current_description).strip(),
                }
            )

        return (
            descriptions
            if descriptions
            else [{"name": "test_generated", "description": content.strip()}]
        )
