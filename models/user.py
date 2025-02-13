from enum import Enum
from pydantic import BaseModel

class UserRoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class UserData(BaseModel):
    user_id: str
    user_name: str
    role: str