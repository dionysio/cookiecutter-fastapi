import inspect
from typing import Optional

import sqladmin.authentication
from fastapi import HTTPException, status
from fastapi.security import APIKeyCookie
from fastapi_users import models
from fastapi_users.authentication import (
    AuthenticationBackend,
    Authenticator,
    Strategy,
    Transport,
)
from fastapi_users.manager import UserManagerDependency
from fastapi_users.router import ErrorCode
from fastapi_users.types import DependencyCallable
from starlette.requests import Request
from starlette.responses import RedirectResponse

from api.v1.auth import authenticate, current_user, get_token


class SessionTransport(Transport):
    """
    Modified version of CookieTransport which simply reads cookies
    and returns tokens instead of full Responses
    """

    scheme: APIKeyCookie

    def __init__(self, name: str = "fastapiusersauth"):
        super().__init__()
        self.scheme = APIKeyCookie(name=name, auto_error=False)

    async def get_login_response(self, token: str) -> str:
        return token

    async def get_logout_response(self):
        pass

    @staticmethod
    def get_openapi_login_responses_success():
        return {}

    @staticmethod
    def get_openapi_logout_responses_success():
        return {}


class FastapiUsersAuthenticationBackend(sqladmin.authentication.AuthenticationBackend):
    def __init__(
        self,
        secret_key: str,
        get_user_manager: UserManagerDependency[models.UP, models.ID],
        get_strategy: DependencyCallable[Strategy[models.UP, models.ID]],
        requires_verification: bool = False,
        name: str = "admin",
    ):
        super().__init__(secret_key)
        self.backend = AuthenticationBackend(
            name=name,
            transport=SessionTransport(),
            get_strategy=get_strategy,
        )
        self.requires_verification = requires_verification
        self.authenticator = Authenticator([self.backend], get_user_manager)

    def _redirect_to_login(self, request: Request):
        return RedirectResponse(request.url_for("admin:login"), status_code=302)

    def _validate_user(self, user):
        # code adjusted from fastapi_users.router.auth.login
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
            )
        if self.requires_verification and not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_USER_NOT_VERIFIED,
            )
        if not user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="LOGIN_USER_NOT_SUPERUSER",
            )

    async def _call_sync_async(self, func, *args, **kwargs):
        if inspect.iscoroutinefunction(func):
            return await func()
        else:
            return func()

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")
        if not token:
            return self._redirect_to_login(request)

        user = await current_user(self.backend, token)

        try:
            self._validate_user(user)
        except HTTPException:
            return self._redirect_to_login(request)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        user = await authenticate(
            username=form.get("username"), password=form.get("password")
        )
        self._validate_user(user)

        request.session["token"] = await get_token(user)
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True
