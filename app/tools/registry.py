from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any


ToolFn = Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]


@dataclass
class ToolSpec:
    name: str
    description: str
    tags: list[str]
    func: ToolFn


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        self._tools[spec.name] = spec

    def get(self, name: str) -> ToolSpec:
        if name not in self._tools:
            raise KeyError(f"tool not found: {name}")
        return self._tools[name]

    def list_tools(self) -> list[ToolSpec]:
        return list(self._tools.values())
