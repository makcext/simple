# flake8: noqa: E501
import logging

import json_log_formatter
from django.conf import settings


# class DramatiqWorkerFilter(logging.Filter):
#     def filter(self, record):
#         if (
#             settings.ENV == "test"
#             and record.name == "dramatiq.worker.Worker"
#             and record.msg in ["Shutting down...", "Worker has been shut down."]
#         ):
#             return False
#         return True


class JSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        extra.update(
            {
                "source": "django",
                "name": record.name,
                "level": record.levelname,
                "processName": record.processName,
                "threadName": record.threadName,
                "filename": record.filename,
                "pathname": record.pathname,
                "funcName": record.funcName,
                "lineno": record.lineno,
                "raddr": record.raddr if hasattr(record, "raddr") else "",
                "env": settings.ENV,
            }
        )
        return super().json_record(message, extra, record)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "timestamp": {
            "format": "[{asctime}][{processName}][{levelname}]: {message}",
            "style": "{",
        },
        "json": {
            "()": "simple.settings.logging.JSONFormatter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "level": "DEBUG",
        },
        "api_file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/api.log",
            "formatter": "json",
            "maxBytes": 1024 * 1024 * 100,  # 100 MB
            "backupCount": 10,
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/django.log",
            "formatter": "json",
            "maxBytes": 1024 * 1024 * 10,
            "backupCount": 5,
        },
        "file_request": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/request.log",
            "formatter": "json",
            "maxBytes": 1024 * 1024 * 10,
            "backupCount": 5,
        },
        "file_server": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/server.log",
            "formatter": "json",
            "maxBytes": 1024 * 1024 * 10,
            "backupCount": 5,
        },
        "file_backends": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/backends.log",
            "formatter": "json",
            "maxBytes": 1024 * 1024 * 10,
            "backupCount": 5,
        },
        "apscheduler": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/apscheduler.log",
            "formatter": "json",
            "maxBytes": 1024 * 1024 * 10,
            "backupCount": 5,
        },
    },
    "loggers": {
        "api": {
            "propagate": False,
            "level": "DEBUG",
            "handlers": ["api_file", "console"],
        },
        "backends": {
            "propagate": False,
            "level": "DEBUG",
            "handlers": ["file_backends", "console"],
        },
        "django": {
            "propagate": False,
            "level": "INFO",
            "handlers": ["file", "console"],
        },
        "django.request": {
            "propagate": False,
            "level": "INFO",
            "handlers": ["file_request", "console"],
        },
        "django.server": {
            "propagate": False,
            "level": "INFO",
            "handlers": ["file_server", "console"],
        },
        "apscheduler": {
            "propagate": False,
            "level": "INFO",
            "handlers": ["apscheduler", "console"],
        },
    },
}

LOG_VIEWER_FILES_DIR = "logs/"
LOG_VIEWER_PAGE_LENGTH = 100
LOG_VIEWER_FILE_LIST_MAX_ITEMS_PER_PAGE = 100
LOG_VIEWER_PATTERNS = ["["]
