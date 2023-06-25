from enum import IntEnum
from typing import Dict, List, Optional

from .base_model import BaseModel


class ErrorCode(IntEnum):
    spanner = 1
    wrench = 2


class ErrorResponseSchema(BaseModel):
    """
    Error response format
    """

    code: int
    message: Optional[str]
    fields: List[Dict] = []


class InternalErrorSchema(ErrorResponseSchema):
    code: int = 500
    message: str = "Internal Server Error"


class NotFoundErrorSchema(ErrorResponseSchema):
    code: int = 404
    message: str = "Not found"


class AuthenticationErrorSchema(ErrorResponseSchema):
    code: int = 401
    message: str = "Invalid credentials"


class AuthorizationErrorSchema(ErrorResponseSchema):
    code: int = 403
    message: str = "You're not allowed to do this"


class ValidationErrorSchema(ErrorResponseSchema):
    code: int = 400
    message: str = "Wrong parameters"


class TooManyRequestsSchema(ErrorResponseSchema):
    code: int = 429
    message: str = "Slow down please"


class ORJsonResponseSchema(BaseModel):
    status_code: Optional[int]
    headers: Optional[Dict]
    content: ErrorResponseSchema
