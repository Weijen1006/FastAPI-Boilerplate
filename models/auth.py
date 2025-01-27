from pydantic import BaseModel

class AuthLoginRequest(BaseModel):
    user_name: str