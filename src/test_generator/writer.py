from pathlib import Path
from typing import List, Dict


class TestFileWriter:
    def __init__(self, output_path: str):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
    
    def write(self, test_code: str) -> None:
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(test_code)
    
    def write_multiple(self, tests: List[Dict[str, str]]) -> None:
        all_tests = []
        imports_set = set()
        
        for test in tests:
            code = test['code']
            test_lines = code.splitlines()
            
            for line in test_lines:
                if line.startswith('import ') or line.startswith('from '):
                    imports_set.add(line)
            
            test_body = '\n'.join([
                line for line in test_lines
                if not (line.startswith('import ') or line.startswith('from '))
            ]).strip()
            
            if test_body:
                all_tests.append(test_body)
        
        final_code = '\n'.join(sorted(imports_set)) + '\n\n\n' + '\n\n\n'.join(all_tests)
        
        self.write(final_code)
