from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
import uvicorn
from controllers.items import router as item_router
from controllers.responses import router as response_router
from utils.logger import LoggerUtils, logger
from models.exception import APIErrorException
from middlewares.request_logger import LogRequestHandler
from middlewares.exceptions import APIExceptionHandler, HTTPExceptionHandler, GlobalExceptionHandler, DataValidationExceptionHandler
from configs import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    LoggerUtils.set_config()
    logger.critical("Application Startup")
    yield
    logger.critical("Application Shutdown")

app = FastAPI(
    title="FastAPI Template",
    lifespan=lifespan
)

app.middleware("http")(LogRequestHandler)

app.add_exception_handler(APIErrorException, APIExceptionHandler)
app.add_exception_handler(HTTPException, HTTPExceptionHandler)
app.add_exception_handler(RequestValidationError, DataValidationExceptionHandler)
app.add_exception_handler(Exception, GlobalExceptionHandler)

@app.get("/")
async def read_root():
    logger.info("Hello World")
    return {"Hello": "World"}

@app.get("/health")
async def health_check():
    return {"status" : "OK"}

@app.get("/info")
async def app_info():
    return {
        "app_name": settings.APP_NAME,
        "api_prefix": settings.API_PREFIX
    } 

app.include_router(router=item_router, prefix=f"{settings.API_PREFIX}/items", tags=["Items"])
app.include_router(router=response_router, prefix=f"{settings.API_PREFIX}/responses", tags=["Responses"])

if __name__ == "__main__":
    reload = True if settings.IS_DEBUG else False
    uvicorn.run(app="main:app", host="0.0.0.0", port=int(settings.APP_PORT), reload=reload, lifespan="on")