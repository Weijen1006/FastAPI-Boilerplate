from typing import Dict

class APIErrorException(Exception):
    def __init__(self, message: str, data: Dict = None, error_object: Dict = None, status_code: int = 400) -> None:
        self.status = "error"
        self.statusCode = status_code
        self.message = message
        self.data = data
        self.errorObject = error_object
