import os
import random
import urllib
import vk_api as vk
import dialogflow_functions
import logging
import telegram

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from urllib.error import HTTPError


logger = logging.getLogger("error_logging")


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot, user_id):
        super().__init__()
        self.bot = bot
        self.user_id = user_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(self.user_id, log_entry)


def answer(event, vk_api, project_id):
    intent_text, is_fallback = dialogflow_functions.detect_intent_text(project_id, event.user_id, event.text, 'ru')
    if not is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=intent_text,
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()

    tg_controlbot = telegram.Bot(os.environ.get('TELEGRAM_CONTROLBOT_TOKEN'))
    tg_user_id = os.environ.get('TELEGRAM_USER_ID')

    logger_settings = TelegramLogsHandler(tg_controlbot, tg_user_id)
    logger_settings.setLevel(logging.INFO)
    logger_settings.setFormatter(logging.Formatter("%(asctime)s: %(levelname)s; %(message)s",
                                                   datefmt="%d/%b/%Y %H:%M:%S"))
    logger.addHandler(logger_settings)

    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    vk_token = os.getenv('VK_TOKEN')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                answer(event, vk_api, project_id)
            except urllib.error.HTTPError as error:
                logger.error(f'VK-бот упал с ошибкой: {error} {error.url}')
            except Exception as error:
                logger.error(f'VK-бот упал с ошибкой: {error}')


if __name__ == '__main__':
    main()
