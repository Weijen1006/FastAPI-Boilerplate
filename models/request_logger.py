from pydantic import BaseModel
from datetime import datetime

class LogRequest(BaseModel):
    requestId: str
    requestHeader: str
    requestBody: str
    responseStatus: int
    responseBody: str
    dateCreated: datetime
    executionTime: float