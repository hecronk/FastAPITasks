from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, Session, sessionmaker

from src.core.settings.settings import settings


# создаём engine
Base = declarative_base()
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True
)
sync_engine = create_engine(
    settings.database_sync_url,
    echo=settings.debug,
    future=True
)
Base.metadata.bind = engine

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession,
)
SessionLocal = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=Session,
)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@contextmanager
def get_sync_session():
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()  # коммит после выполнения задачи
    except Exception:
        session.rollback()  # откат при ошибке
        raise
    finally:
        session.close()
