from pydantic import BaseModel
from typing import Any, Optional, List, Dict, Union
from fastapi.encoders import jsonable_encoder

class Pagination(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    items_per_page: int

class APISuccessResponse(BaseModel):
    status: str = "success"
    statusCode: int = 200
    data: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]] = []
    message: Optional[str] = "success"

    def __init__(self, status: str = "success", status_code: int = 200, message: str = "success", data: Any = None):
        super().__init__()
        self.status = "success"
        self.statusCode = status_code
        self.message = message
        if data:
            self.data = jsonable_encoder(data)

class APIErrorResponse(BaseModel):
    status: str = "error"
    statusCode: int = 400
    data: Optional[Union[List[Dict[str, Any]], Dict[str,Any]]] = []
    message: Optional[str] = "error"
    errorObject: Optional [Dict[str, Any]] = None
    requestId: str