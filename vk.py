import os
import random
import urllib
import vk_api as vk
import functions

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from urllib.error import HTTPError


def check_vk_request_error(response):
    error_code = 0
    if 'error' in str(response):
        error_message = response['error']['error_msg']
        if response['error']['error_code']:
            error_code = response['error']['error_code']
        raise HTTPError(
            'https://dev.vk.com/ru/method/messages.send#Коды%20ошибок',
            error_code,
            'Ошибка сервиса ВКонтакте',
            error_message,
            None
        )


def answer(event, vk_api, project_id):
    intent_texts, is_fallback = functions.detect_intent_texts(project_id, event.user_id, (event.text, ), 'ru')
    if not is_fallback:
        intent_texts = [x.encode('utf-8').decode() for x in intent_texts]
        response = vk_api.messages.send(
            user_id=event.user_id,
            message=''.join(intent_texts),
            random_id=random.randint(1, 1000)
        )
        check_vk_request_error(response)


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
                logger.error(f'{error} {error.url}')


if __name__ == '__main__':
    main()
