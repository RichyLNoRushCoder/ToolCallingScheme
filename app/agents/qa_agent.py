from app.agents.base import AgentContext, AgentResult, BaseAgent


class QAAgent(BaseAgent):
    name = "qa"

    async def run(self, ctx: AgentContext) -> AgentResult:
        risk_flags = []
        quality = ctx.tool_outputs.get("data_quality_checker", {})
        if quality.get("risk_level") == "high":
            risk_flags.append("Data quality risk is high; verify source tables before decision-making.")

        anomaly = ctx.tool_outputs.get("anomaly_detector", {})
        if len(anomaly.get("anomaly_points", [])) > 5:
            risk_flags.append("High number of anomalies detected; run segmented root-cause analysis.")

        if not risk_flags:
            risk_flags.append("No blocking risk found by QA checks.")

        final = "QA Review:\n- " + "\n- ".join(risk_flags)
        return AgentResult(summary=final)
