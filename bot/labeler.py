from config import *
from .bot import bot

router = APIRouter(
    prefix="/callback",
    tags=["callback"],
)

@router.post("/")
async def callback_handler(request: Request, background_task: BackgroundTasks):
    try:
        data = await request.json()

        if data["type"] == "confirmation":
            return PlainTextResponse(CALLBACK_CONFIRMATION)
        elif data["secret"] == CALLBACK_SECRET:
            background_task.add_task(bot.process_event, data)
            
        return { "response": "ok" }
    except Exception:
        raise HTTPException(status_code=403, detail="Forbidden")