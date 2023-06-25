import typing
from contextlib import asynccontextmanager

from fastapi import Depends
from redis.asyncio import Redis

from core.config import settings


async def get_cache(redis_url: str = settings.REDIS_URL, **kwargs) -> Redis:
    session = None
    try:
        session = await Redis.from_url(
            redis_url, encoding="utf8", decode_responses=True, **kwargs
        )
        yield session
    finally:
        if session:
            await session.close()


# reusable fastapi dependency
Cache = typing.Annotated[Redis, Depends(get_cache)]
get_cache_context = asynccontextmanager(get_cache)
