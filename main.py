import logging
import os
from run import detect_intent_texts
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


load_dotenv()
telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_user_id = os.getenv('TELEGRAM_USER_ID')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text('Здравствуйте')


def echo(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.text)


def answer(update: Update, context: CallbackContext):
    answer_texts = detect_intent_texts('mulch-uqka', telegram_user_id, (update.message.text, ), 'ru-RU')
    if answer_texts[0]:
        answer_texts = [x.encode('utf-8').decode() for x in answer_texts]
        update.message.reply_text(''.join(answer_texts))


def main():
    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
