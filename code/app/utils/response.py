# app/utils.py
from typing import Any, Dict, Optional,Union,List
from pydantic import BaseModel

class ApiResponse(BaseModel):
    status: str
    message: str
    status_code: int
    data: Optional[Union[Dict[str, Any], List[Any]]] = None
    error: Optional[Dict[str, Any]] = None

class SuccessResponse(ApiResponse):
    def __init__(self, message: str, data: Optional[Union[Dict[str, Any], List[Any]]] = None):
        super().__init__(status="success", message=message, status_code=200, data=data)

class CreatedResponse(ApiResponse):
    def __init__(self, message: str, data: Optional[Union[Dict[str, Any], List[Any]]] = None):
        super().__init__(status="success", message=message, status_code=201, data=data)

class NoContentResponse(ApiResponse):
    def __init__(self, message: str):
        super().__init__(status="success", message=message, status_code=204)

class BadRequestResponse(ApiResponse):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        error = {
            "code": 400,
            "message": message,
            "details": details
        }
        super().__init__(status="error", message=message, status_code=400, error=error)

class UnauthorizedResponse(ApiResponse):
    def __init__(self, message: str):
        error = {
            "code": 401,
            "message": message
        }
        super().__init__(status="error", message=message, status_code=401, error=error)

class ForbiddenResponse(ApiResponse):
    def __init__(self, message: str):
        error = {
            "code": 403,
            "message": message
        }
        super().__init__(status="error", message=message, status_code=403, error=error)

class NotFoundResponse(ApiResponse):
    def __init__(self, message: str):
        error = {
            "code": 404,
            "message": message
        }
        super().__init__(status="error", message=message, status_code=404, error=error)

class InternalServerErrorResponse(ApiResponse):
    def __init__(self, message: str):
        error = {
            "code": 500,
            "message": message
        }
        super().__init__(status="error", message=message, status_code=500, error=error)
