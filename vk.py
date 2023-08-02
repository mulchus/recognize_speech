import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from main import vk_token, project_id
from run import detect_intent_texts


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )


def answer(event, vk_api):
    intent_texts, is_fallback = detect_intent_texts(project_id, event.user_id, (event.text, ), 'ru')
    if not is_fallback:
        intent_texts = [x.encode('utf-8').decode() for x in intent_texts]
        vk_api.messages.send(
            user_id=event.user_id,
            message=''.join(intent_texts),
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer(event, vk_api)
