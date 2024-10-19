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
    status_code: int = 200
    data: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]] = []
    message: Optional[str] = "success"
    pagination: Optional[Pagination] = None

    def __init__(self, status: str = "success", status_code: int = 200, message: str = "success", data: Any = None):
        super().__init__()
        self.status = "success"
        self.status_code = status_code
        self.message = message
        if data:
            self.data = jsonable_encoder(data)

class APIErrorResponse(BaseModel):
    status: str = "error"
    status_code: int = 400
    data: Optional[Union[List[Dict[str, Any]], Dict[str,Any]]] = []
    message: Optional[str] = "error"
    error_object: Optional [Dict[str, Any]] = None
    request_id: str

class HTTPErrorDetails(BaseModel):
    message: Optional[str] = None
    details: Optional[str] = None
    timestamp: Optional[str] = None
    path: Optional[str] = None
    request_body: Optional[str] = None
    request_header: Optional[str] = None

class HTTPErrorResponse(BaseModel):
    status: str = "error"
    status_code: int = "400"
    error: HTTPErrorDetails
    request_id: str