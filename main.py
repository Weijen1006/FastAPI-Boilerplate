
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from controllers.items import router as item_router
from controllers.responses import router as response_router
from utils.logger import LoggerUtils, logger
from models.exception import APIErrorException
from middlewares.exceptions import APIExceptionHandler

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

app.add_exception_handler(APIErrorException, APIExceptionHandler)

@app.get("/")
def read_root():
    logger.info("Hello World")
    return {"Hello": "World"}

app.include_router(router=item_router, prefix="/v1/items", tags=["Items"])
app.include_router(router=response_router, prefix="/v1/responses", tags=["Responses"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, lifespan="on")