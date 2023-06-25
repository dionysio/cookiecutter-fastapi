import os
import sys
from typing import Any, Dict, Optional

from pydantic import AnyHttpUrl, BaseSettings, RedisDsn, validator


class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(os.path.dirname(__file__))
    ENVIRONMENT: str = "dev"
    DEBUG: bool = ENVIRONMENT == "dev"
    TEST: Optional[bool]
    PROD: bool = ENVIRONMENT == "prod"
    VERSION: str = "0.1"
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"
    PROJECT_NAME: str = "{{cookiecutter.project_name}}"
    LOG_LEVEL: Optional[str]
    BASE_URL: str = ""

    REDIS_URL: Optional[RedisDsn] = RedisDsn(
        url="redis://localhost:6379", scheme="redis"
    )
    DATABASE_URL: str = "postgresql+asyncpg://admin:admin@localhost:5432/{{cookiecutter.project_name}}"
    ASYNC_DATABASE_URL: Optional[str]
    DATABASE_LOCK_TIMEOUT: int = 3  # seconds
    DATABASE_CONNECT_TIMEOUT: int = 10  # seconds
    DATABASE_APPLICATION_NAME: str = f"{PROJECT_NAME}-{ENVIRONMENT}"
    DATABASE_CONNECT_ARGS: Optional[Dict]

    @validator("BASE_URL", pre=True)
    def base_url(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if values.get("DEBUG") or values.get("TEST"):
            return "http://localhost:8000"
        else:
            return "https://{{cookiecutter.project_name}}.app"

    @validator("TEST", pre=True)
    def assemble_test(cls, v: Optional[bool]) -> Any:
        if isinstance(v, bool):
            return v
        return "pytest" in sys.argv[0]

    @validator("LOG_LEVEL", pre=True)
    def assemble_log_level(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return "DEBUG" if values.get("DEBUG") or values.get("TEST") else "INFO"

    @validator("ASYNC_DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        if values.get("TEST"):
            url = "postgresql+asyncpg://admin:admin@localhost:5432/{{cookiecutter.project_name}}_test"
        else:
            url = values["DATABASE_URL"]
            if url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+asyncpg://")
        return url

    @validator("DATABASE_CONNECT_ARGS", pre=True)
    def assemble_db_connect_args(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if "sqlite" in values.get("ASYNC_DATABASE_URL"):
            return {}
        options = f"-c lock_timeout={values.get('DATABASE_LOCK_TIMEOUT') * 1000}"
        return {
            "timeout": values.get("DATABASE_CONNECT_TIMEOUT"),
            "server_settings": {
                "application_name": values.get("DATABASE_APPLICATION_NAME"),
                "options": options,
            },
        }

    SECRET_KEY: str = "{{cookiecutter.secret_key}}"  # make sure to set this to a secure random value when deploying
    BACKEND_CORS_ORIGINS: list[str] | list[AnyHttpUrl] = ["*"]
    NEW_RELIC_LICENSE_KEY: str = ""
    NEW_RELIC_APP_NAME: str = PROJECT_NAME
    JWT_TOKEN_EXPIRATION_TIME = 60 * 60 * 24 * 14  # 14 days

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True


settings = Settings()
