from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from models.exception import APIErrorException
from models.response import APIErrorResponse
from utils.logger import logger

async def APIExceptionHandler(request: Request, exception: APIErrorException):
    error_id = getattr(request.state, "requestId", "")
    logger.error(f"API Response Error")
    response = APIErrorResponse(
        status = "error",
        statusCode= exception.statusCode if isinstance(exception, APIErrorException) else 500,
        message= exception.message,
        data = None,
        errorObject= exception.errorObject,
        requestId=error_id
    )

    content = response.model_dump()

    return JSONResponse(status_code= response.statusCode, content=content)