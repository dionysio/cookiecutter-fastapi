from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

from api import admin_router, api_router_v1, health_router, root_router
from core.config import settings
from core.exceptions import error_responses, setup_exception_handlers
from core.middleware import URLPlugin

# Core Application Instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    openapi_url="/admin/docs/openapi.json",
    redoc_url="/admin/docs",
    default_response_class=ORJSONResponse,
    docs_url=None,
    servers=[
        {
            "url": settings.BASE_URL,
        }
    ],
)
app.add_middleware(
    RawContextMiddleware,
    plugins=(
        plugins.RequestIdPlugin(),
        plugins.UserAgentPlugin(),
        plugins.ForwardedForPlugin(),
        URLPlugin(),
    ),
)

# Set all CORS origins enabled
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Add Routers
app.include_router(api_router_v1, prefix=settings.API_V1_STR, responses=error_responses)
app.include_router(health_router)
app.mount("/admin", admin_router)
app.include_router(root_router, include_in_schema=False)

setup_exception_handlers(app)
