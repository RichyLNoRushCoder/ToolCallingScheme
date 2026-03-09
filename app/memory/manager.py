from collections import defaultdict, deque
from typing import Any

from app.core.config import settings


class MemoryManager:
    """Per-user short-term memory for previous analysis requests."""

    def __init__(self) -> None:
        self._mem: dict[str, deque[dict[str, Any]]] = defaultdict(
            lambda: deque(maxlen=settings.max_memory_items)
        )

    def append(self, user_id: str, item: dict[str, Any]) -> None:
        self._mem[user_id].append(item)

    def recent(self, user_id: str) -> list[dict[str, Any]]:
        return list(self._mem[user_id])
