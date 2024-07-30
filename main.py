from config import *
import bot
import api

app = FastAPI(default_response_class=OrderedJSONResponse)

app.router.include_router(bot.router)
app.router.include_router(api.main_router)

@app.exception_handler(StarletteHTTPException)
async def exception_handler(request: Request, exception: StarletteHTTPException):
    return OrderedJSONResponse(
        {
            "error": str(exception.detail)
        },
        status_code=exception.status_code
    )

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
    # uvicorn.run(app)
    # uvicorn.run(app, host="0.0.0.0", port=8000)