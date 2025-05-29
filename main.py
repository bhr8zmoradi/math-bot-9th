from telegram.ext import Updater
from config import BOT_TOKEN

def start(update, context):
    update.message.reply_text("سلام! به ربات ریاضی نهم خوش آمدید.")

updater = Updater(BOT_TOKEN)
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.start_polling()
