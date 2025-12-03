from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from src.core.settings.settings import get_settings


# создаём engine
Base = declarative_base()
engine = create_async_engine(get_settings().database_url, echo=get_settings().debug, future=True)
Base.metadata.bind = engine

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession,
)

# dependency для FastAPI
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
