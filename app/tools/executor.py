import asyncio
from typing import Any

from app.core.config import settings
from app.schemas import ToolCallRecord
from app.tools.registry import ToolRegistry
from app.utils.errors import ToolExecutionError
from app.utils.retry import retry_async


class ToolExecutor:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    async def execute(self, tool_name: str, payload: dict[str, Any]) -> ToolCallRecord:
        try:
            spec = self.registry.get(tool_name)
        except KeyError as exc:
            return ToolCallRecord(tool_name=tool_name, status="failed", error=str(exc))

        async def _run() -> dict[str, Any]:
            return await asyncio.wait_for(spec.func(payload), timeout=settings.tool_timeout_seconds)

        try:
            result = await retry_async(_run, attempts=settings.max_tool_retries + 1)
            return ToolCallRecord(tool_name=tool_name, status="success", output=result)
        except asyncio.TimeoutError as exc:
            return ToolCallRecord(
                tool_name=tool_name,
                status="failed",
                error=f"timeout after {settings.tool_timeout_seconds}s",
            )
        except Exception as exc:  # noqa: BLE001
            raise ToolExecutionError(tool_name, str(exc)) from exc
