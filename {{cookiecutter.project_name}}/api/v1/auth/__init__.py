from fastapi import APIRouter

from .base import router as base_router
from .endpoints import router as endpoints_router
from .deps import get_strategy, get_user_manager, current_user  # noqa
from .utils import authenticate, get_token, create_user  # noqa

router = APIRouter()
router.include_router(base_router)
router.include_router(endpoints_router)
