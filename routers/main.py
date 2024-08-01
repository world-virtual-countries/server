from config import *

router = APIRouter(
    prefix="",
    tags=["root"],
)

@router.get("/")
async def index_handler():
    return { "response": "alive" }