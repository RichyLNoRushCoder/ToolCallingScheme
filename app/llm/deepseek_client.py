from typing import Any

import httpx

from app.core.config import settings
from app.utils.errors import LLMError


class DeepSeekClient:
    def __init__(self) -> None:
        self.base_url = settings.deepseek_base_url.rstrip("/")
        self.api_key = settings.deepseek_api_key
        self.model = settings.deepseek_model
        self.timeout = settings.llm_timeout_seconds

    async def chat(self, messages: list[dict[str, str]], temperature: float = 0.1) -> str:
        if not self.api_key:
            # Keep development flow available even without key.
            return "[mock-llm] Key missing, running in degraded mode."

        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
        except httpx.TimeoutException as exc:
            raise LLMError("deepseek request timeout") from exc
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text
            raise LLMError(f"deepseek http error: {exc.response.status_code}, {detail}") from exc
        except httpx.HTTPError as exc:
            raise LLMError(f"deepseek network error: {exc}") from exc

        data = resp.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError("invalid deepseek response schema") from exc
