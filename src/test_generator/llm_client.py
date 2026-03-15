"""LLM client for generating test code from descriptions."""

import os
from typing import Optional
import requests


class LLMClient:
    """Client for interacting with GitHub Copilot API (or compatible LLM API)."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        model: str = "gpt-4"
    ):
        """
        Initialize LLM client.
        
        Args:
            api_key: API key for authentication (defaults to GITHUB_TOKEN or OPENAI_API_KEY env var)
            api_base: Base URL for API (defaults to OpenAI or GitHub Models endpoint)
            model: Model to use for generation
        """
        self.api_key = api_key or os.getenv("GITHUB_TOKEN") or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set GITHUB_TOKEN or OPENAI_API_KEY environment variable, "
                "or pass api_key parameter."
            )
        
        # Default to OpenAI-compatible endpoint
        self.api_base = api_base or os.getenv(
            "LLM_API_BASE", 
            "https://api.openai.com/v1"
        )
        self.model = model
        self.timeout = 60
    
    def generate_test_code(self, description: str, context: Optional[str] = None) -> str:
        """
        Generate pytest test code from a text description.
        
        Args:
            description: Natural language description of what to test
            context: Optional additional context (existing code, imports, etc.)
        
        Returns:
            Generated Python test code
        """
        system_prompt = """You are a Python test code generator. Generate clean, well-structured pytest tests.

Requirements:
- Use pytest framework
- Include proper imports
- Add docstrings to test functions
- Use descriptive test names (test_*)
- Include assertions
- Handle edge cases
- Follow PEP 8 style
- Return ONLY the Python code, no explanations or markdown"""

        user_prompt = f"""Generate pytest test code for the following description:

{description}"""

        if context:
            user_prompt += f"\n\nAdditional context:\n{context}"
        
        user_prompt += "\n\nGenerate complete, runnable pytest code:"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.3,  # Lower temperature for more consistent code generation
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            generated_code = result["choices"][0]["message"]["content"]
            
            # Clean up markdown code blocks if present
            generated_code = self._clean_code_output(generated_code)
            
            return generated_code
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to generate test code: {e}")
    
    def _clean_code_output(self, code: str) -> str:
        """Remove markdown code blocks and extra formatting from LLM output."""
        code = code.strip()
        
        # Remove markdown code blocks
        if code.startswith("```python"):
            code = code[len("```python"):].lstrip()
        elif code.startswith("```"):
            code = code[3:].lstrip()
        
        if code.endswith("```"):
            code = code[:-3].rstrip()
        
        return code.strip()
