from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.configs import settings

engine: AsyncEngine = create_async_engine(
    settings.DB_URL,
    echo=settings.DB_ECHO,
    pool_pre_ping=True,
)
async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
    class_=AsyncSession,
)
