from config import *

labeler = BotLabeler()

logger.critical("LABELER INIT")
@labeler.message(text="привет")
async def hi_handler(message: Message):
    logger.critical("RESPONSE")
    users_info = await message.ctx_api.users.get(user_ids=[message.from_id])
    
    await message.answer(
        message=f"Hello, {users_info[0].first_name}",
    )