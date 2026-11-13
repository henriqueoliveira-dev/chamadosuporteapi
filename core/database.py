from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine

from core.configs import settings

engine: AsyncEngine = create_async_engine(settings.DB_URL, echo=True)
async_session: sessionmaker = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    expire_on_commit=False,
    bind=engine, 
    class_=AsyncSession
)
    