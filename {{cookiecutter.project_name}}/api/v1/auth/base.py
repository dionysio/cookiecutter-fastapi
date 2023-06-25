import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport

from models.user import User
from schemas.user import UserCreate, UserRead

from .deps import UserManager, get_strategy

router = APIRouter()


bearer_transport = BearerTransport(tokenUrl="auth/login")
bearer_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_strategy,
)


fastapi_users = FastAPIUsers[User, uuid.UUID](UserManager, [bearer_backend])

current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(
    active=True, superuser=True, optional=True
)
router.include_router(fastapi_users.get_auth_router(bearer_backend))
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
router.include_router(fastapi_users.get_reset_password_router())
router.include_router(
    fastapi_users.get_users_router(UserRead, UserCreate), prefix="/users", tags=["user"]
)
