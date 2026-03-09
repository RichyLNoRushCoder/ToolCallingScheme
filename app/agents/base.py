from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentContext:
    query: str
    user_id: str
    request_id: str
    context: dict[str, Any]
    memory: list[dict[str, Any]] = field(default_factory=list)
    tool_outputs: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    summary: str


class BaseAgent:
    name = "base"

    async def run(self, ctx: AgentContext) -> AgentResult:
        raise NotImplementedError
