import datetime
import logging
import sys
import traceback
from logging.config import dictConfig

import orjson

from core.config import settings
from core.utils import get_pretty_context
from schemas import BaseJsonLogSchema


class JSONLogFormatter(logging.Formatter):
    """
    Custom class-formatter for writing logs to json
    """

    def format(self, record: logging.LogRecord, *args, **kwargs) -> str:
        """
        Formating LogRecord to json
        :param record: logging.LogRecord
        :return: json string
        """
        log_object: dict = self._format_log_object(record)
        return orjson.dumps(log_object).decode()

    @staticmethod
    def _format_log_object(record: logging.LogRecord) -> dict:
        now = (
            datetime.datetime.fromtimestamp(record.created)
            .astimezone()
            .replace(microsecond=0)
            .isoformat()
        )
        message = record.getMessage()
        duration = record.duration if hasattr(record, "duration") else record.msecs
        context_data = get_pretty_context()
        extra = getattr(record, "extra", {})

        json_log_fields = BaseJsonLogSchema(
            thread=record.process,
            timestamp=now,
            level_name=record.levelname,
            message=message,
            source_log=record.name,
            duration=duration,
            app_name=settings.PROJECT_NAME,
            app_version=settings.VERSION,
            app_env=settings.ENVIRONMENT,
            extra=extra,
            **context_data,
        )

        if hasattr(record, "props"):
            json_log_fields.props = record.props

        if record.exc_info:
            json_log_fields.exceptions = (
                # default library traceback
                traceback.format_exception(*record.exc_info)
                # stackprinter gets all debug information
                # https://github.com/cknd/stackprinter/blob/master/stackprinter/__init__.py#L28-L137
            )

        elif record.exc_text:
            json_log_fields.exceptions = record.exc_text

        # Pydantic to dict
        json_log_object = json_log_fields.dict(
            exclude_unset=True,
            by_alias=True,
        )
        # getting additional fields
        if hasattr(record, "request_json_fields"):
            json_log_object.update(record.request_json_fields)

        return json_log_object


def setup_logging():
    log_handler = ["handler"]
    formatter = {}
    if settings.PROD:
        formatter = {
            "()": JSONLogFormatter,
        }
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "formatter": formatter,
        },
        "handlers": {
            "handler": {
                "formatter": "formatter",
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
            }
        },
        "loggers": {
            "main": {
                "handlers": log_handler,
                "level": settings.LOG_LEVEL,
                "propagate": False,
            },
            "uvicorn": {
                "handlers": log_handler,
                "level": settings.LOG_LEVEL,
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": log_handler,
                "level": settings.LOG_LEVEL,
                "propagate": False,
            },
        },
    }

    dictConfig(config)


logger = logging.getLogger("main")
