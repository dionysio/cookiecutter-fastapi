import sqladmin
from fastapi_users.password import PasswordHelper

from api.v1.auth import create_user
from models import User


class UserAdmin(sqladmin.models.ModelView, model=User):
    icon = "fa-solid fa-user"
    column_labels = {User.hashed_password: "Password"}
    column_list = [
        User.id,
        User.email,
        User.is_active,
        User.created_at,
        User.updated_at,
    ]
    column_default_sort = ("updated_at", True)
    column_sortable_list = [User.created_at, User.updated_at]
    column_searchable_list = [User.email, User.first_name, User.last_name]

    async def insert_model(self, data: dict):
        data["password"] = PasswordHelper().hash(data.get("hashed_password"))
        return await create_user(**data)
