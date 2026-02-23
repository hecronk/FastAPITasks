import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.database.db import get_session, Base
from src.main import app


TEST_SCHEMA = "test_schema"

@pytest_asyncio.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(TEST_DB_URL, future=True, echo=False)
    async with engine.begin() as conn:
        await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {TEST_SCHEMA}"))
        await conn.execute(text(f"SET search_path TO {TEST_SCHEMA}"))
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.execute(text(f"DROP SCHEMA {TEST_SCHEMA} CASCADE"))
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(async_engine):
    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        yield s


@pytest_asyncio.fixture
async def client(async_engine):
    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_session():
        async with async_session() as s:
            yield s

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(app=app, base_url="http://testserver") as c:
        yield c

    app.dependency_overrides.clear()
