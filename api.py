from config import *
from bot import bot
import routers

app = FastAPI(default_response_class=OrderedJSONResponse)

app.router.include_router(routers.main.router)
app.router.include_router(routers.callback.router)

@app.on_event("startup")
async def startup_event():
    await bot.setup_webhook()

@app.exception_handler(StarletteHTTPException)
async def exception_handler(request: Request, exception: StarletteHTTPException):
    return OrderedJSONResponse(
        {
            "error": str(exception.detail)
        },
        status_code=exception.status_code
    )
