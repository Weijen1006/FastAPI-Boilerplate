from fastapi import APIRouter, Depends
from typing import Optional, Dict
from utils.logger import LoggerUtils
from auth.auth_handler import AuthHandler
from models.response import APISuccessResponse

router = APIRouter()
logger = LoggerUtils.get_logger(__name__)
auth_handler = AuthHandler()

@router.get("/me")
def read_current_user(current_user: Dict[str, str] | None = Depends(auth_handler.get_current_user)):
    """
    Endpoint to retrieve the current user's information from the JWT token.

    :param current_user: Extracted current user information from the token.
    :return: The current user's info.
    """
    return APISuccessResponse(data=current_user)