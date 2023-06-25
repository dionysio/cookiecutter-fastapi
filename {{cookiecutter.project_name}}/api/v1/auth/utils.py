from fastapi.security import OAuth2PasswordRequestForm

from models import User
from schemas.user import SuperuserUserCreate

from .deps import get_strategy_context, get_user_manager_context


async def create_user(
    email: str, password: str, first_name: str, last_name: str, **kwargs
):
    """
    This utility should only be called from trusted code, not from the user endpoints
    """
    async with get_user_manager_context(expire_on_commit=False) as user_manager:
        return await user_manager.create(
            SuperuserUserCreate(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                **kwargs,
            )
        )


async def update_user(pk, email: str, first_name: str, last_name: str, **kwargs):
    """
    This utility should only be called from trusted code, not from the user endpoints
    """
    async with get_user_manager_context() as user_manager:
        user = await user_manager.get(pk)
        user = await user_manager.update(
            user_update=SuperuserUserCreate(
                email=email, first_name=first_name, last_name=last_name, **kwargs
            ),
            user=user,
            safe=True,
        )
        return user


async def authenticate(username: str, password: str):
    async with get_user_manager_context() as user_manager:
        credentials = OAuth2PasswordRequestForm(
            scope="", username=username, password=password
        )

        return await user_manager.authenticate(credentials)


async def get_token(user: User):
    async with get_strategy_context() as strategy:
        token = await strategy.write_token(user)
    return token
