import json
import re

from app.llm.deepseek_client import DeepSeekClient
from app.tools.registry import ToolRegistry


class ToolRouter:
    """LLM-based router that selects tools from registry based on user query."""

    def __init__(self, registry: ToolRegistry, llm: DeepSeekClient) -> None:
        self.registry = registry
        self.llm = llm

    def _fallback_tools(self) -> list[str]:
        # Conservative fallback to keep analysis chain available.
        return [spec.name for spec in self.registry.list_tools()]

    @staticmethod
    def _extract_json(text: str) -> dict:
        direct = text.strip()
        if direct.startswith("{") and direct.endswith("}"):
            return json.loads(direct)

        fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
        if fenced:
            return json.loads(fenced.group(1))

        generic = re.search(r"(\{.*\})", text, flags=re.DOTALL)
        if generic:
            return json.loads(generic.group(1))
        raise ValueError("no json object found")

    async def route(self, query: str) -> list[str]:
        tools = self.registry.list_tools()
        tool_catalog = [
            {
                "name": spec.name,
                "description": spec.description,
                "tags": spec.tags,
            }
            for spec in tools
        ]

        prompt = (
            "You are a tool routing planner for enterprise data analysis requests. "
            "Select the minimal tool set required to answer the user query.\n"
            "Return JSON only: {\"selected_tools\": [\"tool_a\", \"tool_b\"], \"reason\": \"...\"}\n"
            "Rules:\n"
            "1) selected_tools must contain valid tool names only.\n"
            "2) If uncertain, pick at least one tool.\n"
            "3) Avoid irrelevant tools.\n"
        )

        message = (
            f"User query:\n{query}\n\n"
            f"Available tools:\n{json.dumps(tool_catalog, ensure_ascii=False)}"
        )

        try:
            raw = await self.llm.chat(
                [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": message},
                ],
                temperature=0,
            )
            data = self._extract_json(raw)
            selected = data.get("selected_tools", [])
            valid_names = {spec.name for spec in tools}
            cleaned = [name for name in selected if isinstance(name, str) and name in valid_names]
            if cleaned:
                return cleaned
        except Exception:  # noqa: BLE001
            pass

        return self._fallback_tools()
