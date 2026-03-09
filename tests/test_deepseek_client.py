import httpx
import pytest

from app.llm.deepseek_client import DeepSeekClient
from app.utils.errors import LLMError


@pytest.mark.asyncio
async def test_deepseek_schema_error(monkeypatch) -> None:
    client = DeepSeekClient()
    client.api_key = "x"

    async def handler(request):
        return httpx.Response(200, json={"bad": "schema"})

    transport = httpx.MockTransport(handler)

    class FakeAsyncClient(httpx.AsyncClient):
        def __init__(self, *args, **kwargs):
            kwargs["transport"] = transport
            super().__init__(*args, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", FakeAsyncClient)

    with pytest.raises(LLMError):
        await client.chat([{"role": "user", "content": "hi"}])
