from fastapi import FastAPI, APIRouter
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi.background import BackgroundTasks
from fastapi.responses import Response, JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from vkbottle.bot import Bot, BotLabeler, Message
from vkbottle.callback import BotCallback

from loguru import logger

from typing import Union

import os
import sys
import json
import fastapi
import dotenv
import typing
import jinja2
import loguru
import pendulum
import werkzeug
import vkbottle

dotenv.load_dotenv()

WVC_TOKEN = os.environ.get("WVC_TOKEN")
OUC_TOKEN = os.environ.get("OUC_TOKEN")

CALLBACK_URL = os.environ.get("CALLBACK_URL")
CALLBACK_SERVER_NAME = os.environ.get("CALLBACK_SERVER_NAME")
CALLBACK_CONFIRMATION = os.environ.get("CALLBACK_CONFIRMATION")
CALLBACK_SECRET = os.environ.get("CALLBACK_SECRET")

logger.remove()
logger.add(sys.stdout, format="<level>{level: <8}</level>:     {message}")