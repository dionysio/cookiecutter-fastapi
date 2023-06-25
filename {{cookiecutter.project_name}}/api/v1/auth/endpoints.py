from fastapi import APIRouter, Depends, Response

from .base import bearer_backend, current_active_user
from .deps import get_strategy

router = APIRouter()


@router.post("/refresh")
async def refresh_jwt(
    response: Response,
    strategy=Depends(get_strategy),
    user=Depends(current_active_user),
):
    return await bearer_backend.login(strategy, user, response)
