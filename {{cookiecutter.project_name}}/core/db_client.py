import typing
from contextlib import asynccontextmanager

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from core.config import settings

engine: typing.Optional[AsyncEngine] = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    connect_args=settings.DATABASE_CONNECT_ARGS,
    pool_pre_ping=True,
)


async def cleanup_db_engine():
    global engine
    if engine:
        await engine.dispose()


async def get_db() -> typing.AsyncIterable[AsyncSession]:
    async with AsyncSession(bind=engine) as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


get_db_context = asynccontextmanager(get_db)

# reusable fastapi dependency
Database = typing.Annotated[AsyncSession, Depends(get_db)]
