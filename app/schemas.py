from typing import Any, Literal
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    request_id: str
    user_id: str
    query: str
    context: dict[str, Any] = Field(default_factory=dict)


class ToolCallRecord(BaseModel):
    tool_name: str
    status: Literal["success", "failed"]
    output: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class AgentTrace(BaseModel):
    agent_name: str
    summary: str


class AnalyzeResponse(BaseModel):
    request_id: str
    status: Literal["ok", "partial", "failed"]
    final_answer: str
    agent_traces: list[AgentTrace]
    tool_calls: list[ToolCallRecord]
    warnings: list[str] = Field(default_factory=list)
