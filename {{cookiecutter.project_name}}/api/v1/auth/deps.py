import typing
import uuid
from contextlib import asynccontextmanager

from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.authentication import Authenticator, JWTStrategy

from core import Database, get_db_context
from core.config import settings
from models.user import User, UserDatabase


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    def __init__(self, db: Database):
        super(UUIDIDMixin, self).__init__(user_db=UserDatabase(session=db))


async def get_strategy() -> JWTStrategy:
    yield JWTStrategy(
        secret=settings.SECRET_KEY, lifetime_seconds=settings.JWT_TOKEN_EXPIRATION_TIME
    )


async def get_user_manager() -> typing.AsyncIterable[UserManager]:
    async with get_db_context() as db:
        yield UserManager(db)


get_user_manager_context = asynccontextmanager(get_user_manager)
get_strategy_context = asynccontextmanager(get_strategy)


async def current_user(backend, token: str):
    async with get_strategy_context() as strategy:
        async with get_user_manager_context() as user_manager:
            authenticator = Authenticator([backend], get_user_manager)

            kwargs = {
                "user_manager": user_manager,
                f"strategy_{backend.name}": strategy,
                backend.name: token,
            }
            return await authenticator.current_user(optional=True)(**kwargs)
