from fastapi import APIRouter
from auth.auth_handler import encode_jwt
from utils.logger import LoggerUtils
from models.exception import APIErrorException
from models.auth import AuthLoginRequest
from models.response import APISuccessResponse
from models.user import UserRoleEnum

router = APIRouter()
logger = LoggerUtils.get_logger(__name__)

@router.post("/")
def login(request: AuthLoginRequest):
    logger.info(f"Get user profile: {request.user_name}")
    if request is None:
        raise APIErrorException(status_code=400, message="User profile is empty")
    
    #TODO add mechanism to verify user identity, through username/password in db/redis, OAuth etc

    # Create jwt after the user identity is verified and fetched
    user_data = {"user_id": "1234", "user_name": request.user_name, "role": UserRoleEnum.ADMIN.value}
    token = encode_jwt(user_data)
    logger.info(f"Generated Token: {token}")
    return APISuccessResponse(data=token)
