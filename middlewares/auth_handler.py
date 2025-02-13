from fastapi import HTTPException
from configs.settings import ROLE_HIERARCHY
from models.user import UserData
from functools import wraps
from typing import Callable
from auth.auth_handler import has_permission


def with_role(required_role: str):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user: UserData = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(status_code=403, detail=f"User undefined")
            elif current_user.role not in [role for role in ROLE_HIERARCHY]:
                raise HTTPException(status_code=403, detail=f"Invalid role: {current_user.role}")

            if not has_permission(current_user.role, required_role):
                raise HTTPException(status_code=403, detail=f"Missing permission for: {required_role}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def async_with_role(required_role: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user: UserData = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(status_code=403, detail=f"User undefined")
            elif current_user.role not in [role for role in ROLE_HIERARCHY]:
                raise HTTPException(status_code=403, detail=f"Invalid role: {current_user.role}")

            if not has_permission(current_user.role, required_role):
                raise HTTPException(status_code=403, detail=f"Missing permission for: {required_role}")
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator