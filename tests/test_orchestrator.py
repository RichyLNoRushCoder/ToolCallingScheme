import pytest

from app.agents.analyst_agent import AnalystAgent
from app.agents.base import AgentContext
from app.agents.orchestrator import AgentService
from app.agents.planner import Planner
from app.agents.qa_agent import QAAgent
from app.llm.deepseek_client import DeepSeekClient
from app.tools.builtins import anomaly_detector, data_quality_checker, report_generator
from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry, ToolSpec
from app.tools.router import ToolRouter


class FakeLLM(DeepSeekClient):
    async def chat(self, messages, temperature=0.1):  # type: ignore[override]
        system = messages[0]["content"]
        if "tool routing planner" in system:
            return '{"selected_tools":["data_quality_checker","anomaly_detector","report_generator"],"reason":"full analysis"}'
        return "analyst summary"


@pytest.mark.asyncio
async def test_agent_service_end_to_end() -> None:
    registry = ToolRegistry()
    registry.register(ToolSpec("data_quality_checker", "", ["data"], data_quality_checker))
    registry.register(ToolSpec("anomaly_detector", "", ["data"], anomaly_detector))
    registry.register(ToolSpec("report_generator", "", ["report"], report_generator))

    service = AgentService(
        planner=Planner(),
        tool_router=ToolRouter(registry, FakeLLM()),
        tool_executor=ToolExecutor(registry),
        analyst_agent=AnalystAgent(FakeLLM()),
        qa_agent=QAAgent(),
    )

    ctx = AgentContext(
        query="请给我一份数据质量与异常分析报告",
        user_id="u1",
        request_id="r1",
        context={"row_count": 100, "null_count": 2, "duplicate_count": 1, "time_series": [1, 2, 3, 100]},
    )

    final, traces, tool_calls, warnings = await service.run(ctx)
    assert "analyst summary" in final
    assert len(traces) == 2
    assert len(tool_calls) >= 1
    assert warnings == []
