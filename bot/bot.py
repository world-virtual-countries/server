from config import *

callback = BotCallback(url=CALLBACK_URL, title=CALLBACK_SERVER_NAME)
bot = Bot(token=WVC_TOKEN, callback=callback)

@bot.on.message(text="привет")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(user_ids=[message.from_id])
    await message.answer(f"Hello, {users_info[0].first_name}")