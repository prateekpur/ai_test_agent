from typing import Dict, List

from .llm_client import LLMClient
from .parser import DescriptionParser
from .writer import TestFileWriter


class TestGenerator:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def generate_from_descriptions(
        self, descriptions: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        results = []

        for desc in descriptions:
            test_code = self.llm_client.generate_test_code(
                description=desc["description"], context=None
            )

            results.append(
                {"name": desc["name"], "description": desc["description"], "code": test_code}
            )

        return results

    def generate_from_file(self, input_file: str, output_file: str) -> None:
        parser = DescriptionParser(input_file)
        descriptions = parser.parse()

        tests = self.generate_from_descriptions(descriptions)

        writer = TestFileWriter(output_file)
        writer.write_multiple(tests)
