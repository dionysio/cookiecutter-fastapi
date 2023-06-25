import typing

from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, Session, mapped_column

from models.base import BaseUUIDModel


class User(BaseUUIDModel, SQLAlchemyBaseUserTableUUID):
    __tablename__ = "user"
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()

    def __repr__(self):
        return self.email


class UserDatabase(SQLAlchemyUserDatabase):
    def __init__(self, session: typing.Union[Session, AsyncSession, None] = None):
        super().__init__(session, User)
