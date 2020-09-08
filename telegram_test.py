import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler



My_token = '1297553380:AAHoieUp_G0icaDF9v6QDKTv2G6EPbwM8zU'
updater = Updater(token=My_token, use_context=True)
bot = telegram.Bot(token=My_token)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
print(bot.get_me())

updater.start_polling()
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")