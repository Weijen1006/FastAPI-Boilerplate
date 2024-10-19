from enum import Enum

class ApiErrorMessage(Enum):
    API_RESPONSE_ERROR = "Api Response Error"
    DATA_VALIDATION_ERROR = "Data Validation Error"
    HTTP_ERROR = "Http Error"
    NOT_AUTHENTICATED_ERROR = "Not Authenticated"