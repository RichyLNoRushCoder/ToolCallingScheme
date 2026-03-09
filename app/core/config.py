from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Enterprise Analysis Agent"
    env: str = Field(default="dev", alias="APP_ENV")
    deepseek_api_key: str = Field(default="", alias="DEEPSEEK_API_KEY")
    deepseek_base_url: str = Field(default="https://api.deepseek.com", alias="DEEPSEEK_BASE_URL")
    deepseek_model: str = Field(default="deepseek-chat", alias="DEEPSEEK_MODEL")
    llm_timeout_seconds: int = Field(default=30, alias="LLM_TIMEOUT_SECONDS")
    tool_timeout_seconds: int = Field(default=10, alias="TOOL_TIMEOUT_SECONDS")
    max_tool_retries: int = Field(default=2, alias="MAX_TOOL_RETRIES")
    max_memory_items: int = Field(default=20, alias="MAX_MEMORY_ITEMS")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
