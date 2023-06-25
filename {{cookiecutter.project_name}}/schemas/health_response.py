from .base_model import BaseModel


class HealthResponseSchema(BaseModel):
    """
    Health response format
    """

    database: bool = True
    cache: bool = True


class FailingHealthResponseSchema(BaseModel):
    """
    Health response format
    """

    database: bool = False
    cache: bool = False
