import os

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update, ForceReply


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def echo(update, context):
    update.message.reply_text(update.message.text)


if __name__ == '__main__':
    load_dotenv()
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()
    updater.idle()
