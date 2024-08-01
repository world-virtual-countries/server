from fastapi import FastAPI, APIRouter
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi.background import BackgroundTasks
from fastapi.responses import Response, JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from vkbottle.bot import Bot, BotLabeler, Message
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
callback_confirmation = os.environ.get("CALLBACK_CONFIRMATION")
callback_secret = os.environ.get("CALLBACK_SECRET")

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