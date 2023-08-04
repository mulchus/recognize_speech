import os
import time
import functions

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from telegram.error import NetworkError, TelegramError


def answer(update: Update, context: CallbackContext):
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    telegram_user_id = os.getenv('TELEGRAM_USER_ID')
    logger = functions.set_logger()
    intent_text, _ = functions.detect_intent_text(project_id, telegram_user_id, update.message.text, 'ru')
    try:
        update.message.reply_text(intent_text)
    except (ConnectionError, NetworkError, TelegramError) as error:
        logger.error(f'Потеря или ошибка соединения Телеграм-бота. {error}')
        time.sleep(5)
    except Exception as err:
        logger.error(f'Телеграм-бот упал с ошибкой: {err}')


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
