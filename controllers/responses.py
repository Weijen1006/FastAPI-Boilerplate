from fastapi import FastAPI, HTTPException, APIRouter
from models.response import APISuccessResponse
from models.exception import APIErrorException
from models.sample_data import sample_data
from utils.logger import logger

router = APIRouter()

@router.get("/api_success")
def get_success_response():
    logger.info(f"Sample Success Response")
    return APISuccessResponse(data=sample_data)

@router.get("/api_error")
def get_error_response():
    logger.info(f"Sample API Error Response")
    raise APIErrorException(message="Sample API Error Response")