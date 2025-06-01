from fastapi import HTTPException
from configs.settings import ROLE_HIERARCHY
from models.user import UserData
from functools import wraps
from typing import Callable
from auth.auth_handler import has_permission
import asyncio


def with_role(required_role: str):
    def decorator(func: Callable):

        def check_permission(kwargs):
            current_user: UserData = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(status_code=403, detail=f"User undefined")
            elif current_user.role not in [role for role in ROLE_HIERARCHY]:
                raise HTTPException(status_code=403, detail=f"Invalid role: {current_user.role}")

            if not has_permission(current_user.role, required_role):
                raise HTTPException(status_code=403, detail=f"Missing permission for: {required_role}")

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            check_permission(kwargs)
            return await func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            check_permission(kwargs)
            return func(*args, **kwargs)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    return decorator