import datetime
import uuid

import pydantic


class BaseModel(pydantic.BaseModel):
    pass


class BaseModelUUID(BaseModel):
    id: uuid.UUID
    updated_at: datetime.datetime
    created_at: datetime.datetime

    class Config:
        orm_mode = True
