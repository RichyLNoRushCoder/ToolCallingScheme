import pytest

from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry, ToolSpec


async def _boom(_):
    raise RuntimeError("tool crashed")


@pytest.mark.asyncio
async def test_tool_executor_raises_wrapped_error() -> None:
    registry = ToolRegistry()
    registry.register(ToolSpec("boom", "", [], _boom))
    executor = ToolExecutor(registry)

    with pytest.raises(Exception) as exc:
        await executor.execute("boom", {})
    assert "boom" in str(exc.value)
