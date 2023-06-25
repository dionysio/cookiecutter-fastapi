import sqladmin
from fastapi import APIRouter

from api.v1.auth import get_strategy, get_user_manager
from core import engine
from core.config import settings
from core.exceptions import setup_exception_handlers

from .auth import FastapiUsersAuthenticationBackend

from .user import UserAdmin

router = APIRouter()

admin = sqladmin.Admin(
    router,
    engine,
    authentication_backend=FastapiUsersAuthenticationBackend(
        secret_key=settings.SECRET_KEY,
        get_user_manager=get_user_manager,
        get_strategy=get_strategy,
    ),
    base_url="/",
    title=settings.PROJECT_NAME.title(),
)
for view in (UserAdmin, ):
    admin.add_view(view)
setup_exception_handlers(admin.admin)
