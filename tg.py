import time
import vk
from run import detect_intent_texts
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

from main import telegram_token, telegram_user_id, project_id

bot = Bot(telegram_token)


def send_message(message):
    bot.send_message(telegram_user_id, str(message))


def answer(update: Update, context: CallbackContext):
    intent_texts, is_fallback = detect_intent_texts(project_id, telegram_user_id, (update.message.text, ), 'ru')
    if not is_fallback:
        intent_texts = [x.encode('utf-8').decode() for x in intent_texts]
        try:
            update.message.reply_text(''.join(intent_texts))
        except (ConnectionError, telegram.error.NetworkError, telegram.error.TelegramError) as error:
            vk.send_message(f'Потеря или ошибка соединения Телеграм-бота. {error}')
            time.sleep(5)
        except Exception as err:
            vk.send_message(f'Телеграм-бот упал с ошибкой: {err}')


def main():
    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
