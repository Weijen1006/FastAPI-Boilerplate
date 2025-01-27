from fastapi import HTTPException, APIRouter
from models.response import APISuccessResponse
from models.exception import APIErrorException
from models.sample_data import sample_data
from utils.logger import logger
from configs import constants

router = APIRouter()

@router.get("/api_success")
def get_success_response():
    logger.info(f"Sample Success Response")
    return APISuccessResponse(data=sample_data)

@router.get("/api_error")
def get_error_response():
    logger.info(f"Sample API Error Response")
    raise APIErrorException(message="Sample API Error Response", error_object={"username": "Invalid input"})

@router.get("/http_error")
def get_http_error_response():
    logger.info(f"Sample HTTP Error")
    raise HTTPException(status_code=403, detail=constants.ApiErrorMessage.NOT_AUTHENTICATED_ERROR.value)

@router.get("/other_error")
def get_other_error_response():
    logger.info(f"Sample General Error")
    raise ZeroDivisionError