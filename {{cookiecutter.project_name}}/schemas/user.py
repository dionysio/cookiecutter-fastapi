import uuid
from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.Generic[schemas.models.ID], schemas.CreateUpdateDictModel):
    id: uuid.UUID
    email: schemas.EmailStr
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class UserCreate(schemas.CreateUpdateDictModel):
    email: schemas.EmailStr
    password: str
    first_name: str
    last_name: str


class SuperuserUserCreate(UserCreate):
    is_superuser: bool = False
    password: Optional[str]
