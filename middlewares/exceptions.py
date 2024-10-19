from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from models.exception import APIErrorException
from models.response import APIErrorResponse, HTTPErrorDetails, HTTPErrorResponse
from utils.logger import logger
import uuid, sys
from datetime import datetime
from configs import constants

async def APIExceptionHandler(request: Request, exception: APIErrorException):
    error_id = getattr(request.state, "requestId", "")
    logger.error(f"API Response Error")
    response = APIErrorResponse(
        status="error",
        statusCode=exception.statusCode if isinstance(exception, APIErrorException) else 500,
        message=exception.message,
        data=None,
        errorObject=exception.errorObject,
        requestId=error_id
    )

    content = response.model_dump()

    return JSONResponse(status_code= response.statusCode, content=content)

async def HTTPExceptionHandler(request: Request, exception: HTTPException):
    error_id = getattr(request.state, "requestId", str(uuid.uuid4()))
    error_details = HTTPErrorDetails(
        message=str(exception.detail),
        details=str(exception),
        timestamp=str(datetime.now()),
        path=request.url._url,
        requestBody=await request.body(),
        requestMethod=request.method,
    )
    error_response = HTTPErrorResponse(
        status="error",
        statusCode=exception.status_code if isinstance(exception, HTTPException) else 500,
        error=error_details,
        requestId=error_id,
    )

    content = error_response.model_dump()
    response = JSONResponse(status_code=error_response.statusCode, content= content)

    return response

async def GlobalExceptionHandler(request: Request, exception: Exception):
    logger.error(f"Unexpected error: {exception}", exc_info=True)
    error_id = getattr(request.state, "requestId", "")
    exception_type, exception_value, exception_traceback= sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    body = getattr(request.state, "body", None)
    error_details = HTTPErrorDetails(
        message=str(exception_name),
        details=str(exception_value),
        timestamp=str(datetime.now()),
        path=url,
        requestBody=body,
        requestMethod=request.method,
    )
    error_response = HTTPErrorResponse(
        status="error",
        statusCode=500,
        error=error_details,
        requestId=error_id,
    )

    content = error_response.model_dump()
    response = JSONResponse(status_code=error_response.statusCode, content= content)

    return response

async def DataValidationExceptionHandler(request: Request, exception: RequestValidationError):
    error_response = {}
    for error in exception.errors():
        error_msg = f"{error.get('msg')} - {error.get('type')} at {'.'.join(error.get('loc'))}"
        error_response[error.get("loc")[1]] = error_msg
    
    raise APIErrorException(
        status_code=422,
        message=constants.ApiErrorMessage.DATA_VALIDATION_ERROR.value,
        error_object=error_response
    )