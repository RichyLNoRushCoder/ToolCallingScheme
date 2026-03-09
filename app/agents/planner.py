from dataclasses import dataclass

from app.utils.errors import PlannerError


@dataclass
class PlanStep:
    step_id: str
    owner_agent: str
    description: str


class Planner:
    """Rule-based planner; can be upgraded to LLM planner in future."""

    def build_plan(self, query: str) -> list[PlanStep]:
        if not query.strip():
            raise PlannerError("empty query")

        return [
            PlanStep(step_id="S1", owner_agent="analyst", description="Gather evidence from data tools"),
            PlanStep(step_id="S2", owner_agent="qa", description="Cross-check risks and produce final answer"),
        ]
