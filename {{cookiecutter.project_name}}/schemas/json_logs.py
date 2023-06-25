from typing import List, Union

from pydantic import Field

from .base_model import BaseModelUUID


class BaseJsonLogSchema(BaseModelUUID):
    """
    Main log in JSON format
    """

    thread: Union[int, str]
    level_name: str
    message: str
    source_log: str
    timestamp: str = Field(..., alias="@timestamp")
    app_name: str
    app_version: str
    app_env: str
    duration: int
    exceptions: Union[List[str], str] = None
    trace_id: str = None
    span_id: str = None
    parent_id: str = None

    user_id: str = None
    redis_websocket_key: str = None
    url: str = None
    user_agent: str = None
    forwarded_for: str = None

    class Config:
        allow_population_by_field_name = True
        extra = "allow"
