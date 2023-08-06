import os
import logging
import dialogflow
import telegram

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from dialogflow import TelegramLogsHandler


logger = logging.getLogger("error_logging")


def answer(update: Update, context: CallbackContext):
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    telegram_user_id = os.getenv('TELEGRAM_USER_ID')
    intent_text, _ = dialogflow.detect_intent_text(project_id, telegram_user_id, update.message.text, 'ru')
    update.message.reply_text(intent_text)


def error_handler(update, context):
    logger.error(msg='Телеграм-бот упал с ошибкой:', exc_info=context.error)


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    tg_controlbot = telegram.Bot(os.environ.get('TELEGRAM_CONTROLBOT_TOKEN'))
    tg_user_id = os.environ.get('TELEGRAM_USER_ID')

    logger_settings = TelegramLogsHandler(tg_controlbot, tg_user_id)
    logger_settings.setLevel(logging.INFO)
    logger_settings.setFormatter(logging.Formatter("%(asctime)s: %(levelname)s; %(message)s",
                                                   datefmt="%d/%b/%Y %H:%M:%S"))
    logger.addHandler(logger_settings)

    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))
    dispatcher.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
