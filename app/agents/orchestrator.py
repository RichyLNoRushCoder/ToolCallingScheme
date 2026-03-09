from typing import Any

from app.agents.analyst_agent import AnalystAgent
from app.agents.base import AgentContext
from app.agents.planner import Planner
from app.agents.qa_agent import QAAgent
from app.schemas import AgentTrace, ToolCallRecord
from app.tools.executor import ToolExecutor
from app.tools.router import ToolRouter


class AgentService:
    def __init__(
        self,
        planner: Planner,
        tool_router: ToolRouter,
        tool_executor: ToolExecutor,
        analyst_agent: AnalystAgent,
        qa_agent: QAAgent,
    ) -> None:
        self.planner = planner
        self.tool_router = tool_router
        self.tool_executor = tool_executor
        self.analyst_agent = analyst_agent
        self.qa_agent = qa_agent

    async def run(self, ctx: AgentContext) -> tuple[str, list[AgentTrace], list[ToolCallRecord], list[str]]:
        _plan = self.planner.build_plan(ctx.query)

        tool_names = await self.tool_router.route(ctx.query)
        tool_calls: list[ToolCallRecord] = []
        tool_outputs: dict[str, Any] = {}
        warnings: list[str] = []

        for name in tool_names:
            record = await self.tool_executor.execute(name, {"query": ctx.query, "context": ctx.context})
            tool_calls.append(record)
            if record.status == "success":
                tool_outputs[name] = record.output
            else:
                warnings.append(f"tool_failed:{name}:{record.error}")

        ctx.tool_outputs = tool_outputs

        analyst_res = await self.analyst_agent.run(ctx)
        qa_res = await self.qa_agent.run(ctx)

        traces = [
            AgentTrace(agent_name="analyst", summary=analyst_res.summary),
            AgentTrace(agent_name="qa", summary=qa_res.summary),
        ]

        final_answer = f"{analyst_res.summary}\n\n{qa_res.summary}"
        return final_answer, traces, tool_calls, warnings
