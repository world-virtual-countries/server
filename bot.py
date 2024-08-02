from config import *
import labelers

bot = Bot(token=WVC_TOKEN, callback=BotCallback(url=CALLBACK_URL, title=CALLBACK_SERVER_NAME, secret_key=CALLBACK_SECRET))

bot.labeler.load(labelers.main.labeler)
