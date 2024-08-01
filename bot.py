from config import *
import labelers

callback = BotCallback(url=CALLBACK_URL, title=CALLBACK_SERVER_NAME)
bot = Bot(token=WVC_TOKEN, callback=callback)

bot.labeler.load(labelers.main.labeler)