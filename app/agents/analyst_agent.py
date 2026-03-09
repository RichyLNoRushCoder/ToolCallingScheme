import json

from app.agents.base import AgentContext, AgentResult, BaseAgent
from app.llm.deepseek_client import DeepSeekClient
from app.utils.errors import LLMError


class AnalystAgent(BaseAgent):
    name = "analyst"

    def __init__(self, llm: DeepSeekClient) -> None:
        self.llm = llm

    @staticmethod
    def _fallback_summary(ctx: AgentContext) -> str:
        quality = ctx.tool_outputs.get("data_quality_checker", {})
        anomaly = ctx.tool_outputs.get("anomaly_detector", {})
        report = ctx.tool_outputs.get("report_generator", {})
        return (
            "LLM unavailable. Fallback analytical summary generated from tool outputs.\n"
            f"- Data Quality: {quality}\n"
            f"- Anomaly Detection: {anomaly}\n"
            f"- Report Draft: {report}"
        )

    async def run(self, ctx: AgentContext) -> AgentResult:
        prompt = (
            "You are a senior data analyst. Build a concise analysis from tool outputs. "
            "Highlight data quality, anomalies, and business impact."
        )
        tool_blob = json.dumps(ctx.tool_outputs, ensure_ascii=False)
        memory_blob = json.dumps(ctx.memory[-5:], ensure_ascii=False)
        try:
            content = await self.llm.chat(
                [
                    {"role": "system", "content": prompt},
                    {
                        "role": "user",
                        "content": f"Query: {ctx.query}\nTool Outputs: {tool_blob}\nRecent Memory: {memory_blob}",
                    },
                ]
            )
        except LLMError:
            content = self._fallback_summary(ctx)
        return AgentResult(summary=content)
