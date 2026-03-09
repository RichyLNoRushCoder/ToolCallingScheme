from app.agents.base import AgentContext
from app.agents.orchestrator import AgentService
from app.memory.manager import MemoryManager
from app.schemas import AnalyzeRequest, AnalyzeResponse


class AnalysisService:
    def __init__(self, agent_service: AgentService, memory_manager: MemoryManager) -> None:
        self.agent_service = agent_service
        self.memory_manager = memory_manager

    async def analyze(self, req: AnalyzeRequest) -> AnalyzeResponse:
        memory = self.memory_manager.recent(req.user_id)
        ctx = AgentContext(
            query=req.query,
            user_id=req.user_id,
            request_id=req.request_id,
            context=req.context,
            memory=memory,
        )

        final_answer, traces, tool_calls, warnings = await self.agent_service.run(ctx)
        status = "ok"
        if warnings:
            status = "partial"
        if not final_answer.strip():
            status = "failed"

        self.memory_manager.append(
            req.user_id,
            {
                "request_id": req.request_id,
                "query": req.query,
                "status": status,
                "warnings": warnings,
            },
        )

        return AnalyzeResponse(
            request_id=req.request_id,
            status=status,
            final_answer=final_answer,
            agent_traces=traces,
            tool_calls=tool_calls,
            warnings=warnings,
        )
