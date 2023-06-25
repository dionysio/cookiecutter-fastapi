from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.utils import get_pretty_context
from core.logging import logger


class CatchExceptionsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            return await call_next(request)
        except Exception as e:
            params = get_pretty_context()
            logger.exception(extra=params)
            return JSONResponse({"detail": "Internal server error"}, status_code=500)
