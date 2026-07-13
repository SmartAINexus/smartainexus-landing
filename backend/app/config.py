from functools import lru_cache
from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    auth_mode: Literal["development_header", "oidc"] = "development_header"
    database_url: str = "postgresql+psycopg://grantbridge:change-me@localhost/grantbridge"
    log_level: str = "INFO"
    api_v1_prefix: str = "/api/v1"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @model_validator(mode="after")
    def reject_development_auth_in_production(self) -> "Settings":
        if self.app_env.lower() == "production" and self.auth_mode == "development_header":
            raise ValueError(
                "Production cannot use the untrusted X-Tenant-ID development header; configure OIDC."
            )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
