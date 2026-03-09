from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="CaiHub Backend", alias="CAIHUB_APP_NAME")
    app_version: str = Field(default="0.1.0", alias="CAIHUB_APP_VERSION")
    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        alias="CAIHUB_ENVIRONMENT",
    )
    debug: bool = Field(default=True, alias="CAIHUB_DEBUG")
    api_v1_prefix: str = Field(default="/api/v1", alias="CAIHUB_API_V1_PREFIX")
    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/caihub",
        alias="CAIHUB_DATABASE_URL",
    )
    auto_create_tables: bool = Field(
        default=False,
        alias="CAIHUB_AUTO_CREATE_TABLES",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
