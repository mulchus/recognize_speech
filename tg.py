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
    intent_texts, is_fallback = functions.detect_intent_texts(project_id, telegram_user_id, (update.message.text, ), 'ru')
    if not is_fallback:
        intent_texts = [x.encode('utf-8').decode() for x in intent_texts]
        try:
            update.message.reply_text(''.join(intent_texts))
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
