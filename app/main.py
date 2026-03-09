from fastapi import FastAPI

from app.agents.analyst_agent import AnalystAgent
from app.agents.orchestrator import AgentService
from app.agents.planner import Planner
from app.agents.qa_agent import QAAgent
from app.core.config import settings
from app.gateway.api_gateway import router as gateway_router
from app.llm.deepseek_client import DeepSeekClient
from app.memory.manager import MemoryManager
from app.services.analysis_service import AnalysisService
from app.tools.builtins import anomaly_detector, data_quality_checker, report_generator
from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry, ToolSpec
from app.tools.router import ToolRouter


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.include_router(gateway_router)
    return app


registry = ToolRegistry()
registry.register(
    ToolSpec(
        name="data_quality_checker",
        description="Compute null/duplicate rates and risk level",
        tags=["data", "quality"],
        func=data_quality_checker,
    )
)
registry.register(
    ToolSpec(
        name="anomaly_detector",
        description="Detect outliers from time series",
        tags=["data", "anomaly"],
        func=anomaly_detector,
    )
)
registry.register(
    ToolSpec(
        name="report_generator",
        description="Generate business report sections",
        tags=["report"],
        func=report_generator,
    )
)

llm_client = DeepSeekClient()
planner = Planner()
tool_router = ToolRouter(registry, llm_client)
tool_executor = ToolExecutor(registry)
analyst_agent = AnalystAgent(llm_client)
qa_agent = QAAgent()
memory_manager = MemoryManager()

agent_service = AgentService(
    planner=planner,
    tool_router=tool_router,
    tool_executor=tool_executor,
    analyst_agent=analyst_agent,
    qa_agent=qa_agent,
)
analysis_service = AnalysisService(agent_service=agent_service, memory_manager=memory_manager)

app = create_app()
