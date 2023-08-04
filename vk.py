import os
import random
import urllib
import vk_api as vk
import functions

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from urllib.error import HTTPError


def answer(event, vk_api, project_id):
    intent_text, is_fallback = functions.detect_intent_text(project_id, event.user_id, event.text, 'ru')
    if not is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=intent_text,
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()
    logger = functions.set_logger()
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
