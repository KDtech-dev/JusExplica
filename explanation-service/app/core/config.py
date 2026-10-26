from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "JusExplica - Explanation Service"
    service_description: str = (
        "API responsável por explicar movimentações judiciais "
        "em linguagem simples."
    )
    service_version: str = "0.2.0"
    api_prefix: str = "/v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
