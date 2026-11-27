import os
import httpx
from dotenv import load_dotenv

load_dotenv()


class LLMService:

    def __init__(self):
        # Load inference configuration
        self.base_url = os.getenv(
            "OLLAMA_BASE_URL", "http://localhost:11434"
        )
        self.model = os.getenv(
            "OLLAMA_MODEL", "qwen2.5-coder:3b"
        )
        self.context_window = int(
            os.getenv("OLLAMA_CONTEXT_WINDOW", "4096")
        )
        self.timeout = float(
            os.getenv("OLLAMA_TIMEOUT", "120")
        )

    def generate(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful coding assistant."
    ) -> str:

        # Validate input
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        # Build the inference request
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_ctx": self.context_window,
                "num_predict": 512
            }
        }

        try:
            # Call the local inference API
            response = httpx.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=self.timeout
            )

            # Check for HTTP errors
            response.raise_for_status()

            # Extract generated text
            return response.json()["message"]["content"]

        except httpx.TimeoutException as exc:
            raise RuntimeError("LLM request timed out") from exc

        except httpx.ConnectError as exc:
            raise RuntimeError("Cannot connect to Ollama") from exc

        except httpx.HTTPError as exc:
            raise RuntimeError("LLM request failed") from exc