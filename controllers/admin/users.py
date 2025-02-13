from fastapi import APIRouter, Depends
from utils.logger import LoggerUtils
from auth.auth_handler import get_current_user
from models.response import APISuccessResponse
from models.user import UserData

router = APIRouter()
logger = LoggerUtils.get_logger(__name__)

@router.get("/me")
def read_current_user(current_user: UserData = Depends(get_current_user)):
    """
    Endpoint to retrieve the current user's information from the JWT token.

    :param current_user: Extracted current user information from the token.
    :return: The current user's info.
    """
    return APISuccessResponse(data=current_user)