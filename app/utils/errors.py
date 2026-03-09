class AppError(Exception):
    """Base app-level error."""


class ToolExecutionError(AppError):
    def __init__(self, tool_name: str, message: str):
        self.tool_name = tool_name
        super().__init__(f"[{tool_name}] {message}")


class PlannerError(AppError):
    pass


class LLMError(AppError):
    pass
