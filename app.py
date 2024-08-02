from config import *
import routers

app = FastAPI(default_response_class=JSONResponse)

app.router.include_router(routers.main.router)
app.router.include_router(routers.callback.router)

@app.exception_handler(StarletteHTTPException)
async def exception_handler(request: Request, exception: StarletteHTTPException):
    return JSONResponse(
        {
            "error": str(exception.detail)
        },
        status_code=exception.status_code
    )