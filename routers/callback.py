from config import *
from bot import bot

router = APIRouter(
    prefix="/callback",
    tags=["callback"],
)

@router.post("/", response_class=PlainTextResponse)
async def callback_handler(request: Request, background_task: BackgroundTasks):
    try:
        data = await request.json()
        
        logger.critical("START")
        
        if data["type"] == "confirmation":
            logger.critical("CONFIRMATION")
            return CALLBACK_CONFIRMATION
        if data["secret"] == CALLBACK_SECRET:
            background_task.add_task(bot.process_event, data)
        logger.critical("SECRET")
        logger.critical(data["secret"])
        logger.critical(bot.callback.get_secret_key())
        logger.critical(CALLBACK_SECRET)
            
        logger.critical("END")
            
        return "ok"
    except Exception as e:
        raise HTTPException(status_code=403, detail="Forbidden")