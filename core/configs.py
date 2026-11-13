from typing import ClassVar

from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "mysql+asyncmy://dev:123456@localhost:3306/chamados_suporte"
    DBBaseModel: ClassVar[type] = declarative_base()

    JWT_SECRET: str = "g0tk6H-2TL6Ydy5WFQ6eGePc6jKJ9F-2NczfMevInMk"
    """
    import secrets

    token = secrets.token_urlsafe(32)
    """

    ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 7 days => 1  semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 7

settings: Settings = Settings()        