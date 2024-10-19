from pydantic import BaseModel
from datetime import datetime

class LogRequest(BaseModel):
    request_id: str
    request_header: str
    request_body: str
    response_status: int
    response_body: str
    date_created: datetime
    execution_time: float