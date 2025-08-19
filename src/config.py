import enum
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent


class TaskStatus(str, enum.Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class DatabaseSettings(BaseModel):
    name: str = os.getenv("POSTGRES_DB", "user")
    user: str = os.getenv("POSTGRES_USER", "admin")
    password: str = os.getenv("POSTGRES_PASSWORD", "admin")
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", "5432"))
    url: PostgresDsn = (
        f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"  # type: ignore
    )


class PaginationSettings(BaseModel):
    max_entities_per_page: int = 100


class AppSettings(BaseModel):
    mode: Literal[
        "TEST",
        "LOCAL",
        "DEV",
        "PROD",
    ] = os.getenv("APP_MODE")  # type: ignore


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    db: DatabaseSettings = DatabaseSettings()
    pagination: PaginationSettings = PaginationSettings()


settings = Settings()
