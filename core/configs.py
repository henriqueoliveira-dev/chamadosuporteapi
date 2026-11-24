from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import declarative_base


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    API_V1_STR: str = "/api/v1"
    DB_URL: str = Field(min_length=1)
    DB_ECHO: bool = False
    DBBaseModel: ClassVar[type] = declarative_base()

    # A secret must be supplied by the environment; a committed default would
    # let anyone forge access tokens. Keep at least 256 bits of entropy.
    JWT_SECRET: str = Field(min_length=32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30 * 24 * 7, gt=0)


settings: Settings = Settings()
