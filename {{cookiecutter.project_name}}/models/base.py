import typing
import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class CreatedUpdatedMixin:
    updated_at: Mapped[typing.Optional[datetime]] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )
    created_at: Mapped[typing.Optional[datetime]] = mapped_column(
        default=datetime.utcnow
    )


class BaseUUIDModel(Base, CreatedUpdatedMixin):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
