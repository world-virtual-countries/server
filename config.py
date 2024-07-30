from fastapi import FastAPI, APIRouter
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi.background import BackgroundTasks
from fastapi.responses import Response, JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from vkbottle import Bot
from vkbottle.bot import Message
from vkbottle.callback import BotCallback

from loguru import logger

import os
import sys
import json
import dotenv
import typing
import uvicorn
import logging
import pendulum

dotenv.load_dotenv()

WVC_TOKEN = os.environ.get("WVC_TOKEN")
OUC_TOKEN = os.environ.get("OUC_TOKEN")

CALLBACK_URL = os.environ.get("CALLBACK_URL")
CALLBACK_SERVER_NAME = os.environ.get("CALLBACK_SERVER_NAME")
CALLBACK_CONFIRMATION = os.environ.get("CALLBACK_CONFIRMATION")
CALLBACK_SECRET = os.environ.get("CALLBACK_SECRET")

LOGGER_DATE = pendulum.now("UTC").strftime("%d-%m-%Y")

LOGGER_FILE_FOLDER = "logs/"
LOGGER_FILE_TYPE = ".log"

LOGGER_FILE_ROTATION = "1 day"
LOGGER_FILE_RETENTION = None
LOGGER_FILE_COMPRESSION = None

LOGGER_FILE = f"./data/{LOGGER_FILE_FOLDER}/{LOGGER_DATE}.{LOGGER_FILE_TYPE}"
LOGGER_CONSOLE = sys.stdout

LOGGER_LEVEL = "DEBUG"
LOGGER_FORMAT = "<black>{time: HH:mm:ss!UTC} -</black> <level>{level}:</level> | <green>{name: <15} : {line: >4}</green> | <level>{message}</level>"

class OrderedJSONResponse(JSONResponse):
    media_type = "application/json"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=True,
            indent=4,
        ).encode("utf-8")
        
class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def format_record(record: dict) -> str:
    format_string = LOGGER_FORMAT
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


def init_logging():
    loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn") or name.startswith("watchfiles")
    )
    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = []

    # change handler for default uvicorn logger
    intercept_handler = InterceptHandler()
    logging.getLogger("uvicorn").handlers = [intercept_handler]

    # set logs output, level and format
    logger.configure(
        handlers=[{"sink": sys.stdout, "level": logging.DEBUG, "format": format_record}]
    )
init_logging()

# logger.critical(logging.root.manager.loggerDict)
    