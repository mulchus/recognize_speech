import os
import functions

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext


def answer(update: Update, context: CallbackContext):
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    telegram_user_id = os.getenv('TELEGRAM_USER_ID')
    intent_text, _ = functions.detect_intent_text(project_id, telegram_user_id, update.message.text, 'ru')
    update.message.reply_text(intent_text)


def error_handler(update, context):
    logger = functions.set_logger()
    logger.error(msg='Телеграм-бот упал с ошибкой:', exc_info=context.error)


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))
    dispatcher.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
