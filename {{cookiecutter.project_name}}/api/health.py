from functools import wraps
from typing import Any, Dict

from fastapi import APIRouter
from fastapi_health import health

from core import get_db_context
from core.logging import logger
from schemas import FailingHealthResponseSchema, HealthResponseSchema

router = APIRouter()


async def health_handler(**kwargs) -> Dict[str, Any]:
    return kwargs


def healthcheck(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        healthy = True
        name = func.__name__
        try:
            await func(*args, **kwargs)
        except Exception:
            logger.exception(f"{name} health check failing")
            healthy = False
        finally:
            logger.info(f"{name} health check", extra={"extra": {name: healthy}})
        return healthy

    return wrapper


@healthcheck
async def database():
    async with get_db_context() as db:
        await db.connection()


responses = {
    200: {"model": HealthResponseSchema},
    503: {"model": FailingHealthResponseSchema},
}
router.add_api_route(
    "/health",
    health(
        [database],
        failure_handler=health_handler,
        success_handler=health_handler,
    ),
    name="health",
    responses=responses,
)
