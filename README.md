# Боты распознавания речи в Telegram и VK


## Переменные окружения
Часть настроек проекта берётся из переменных окружения.  
Чтобы их определить, создайте файл `.env` в корневой папке `recognize_speech` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`:    
- `TELEGRAM_BOT_TOKEN` - [Инструкция, как создать бота.](https://core.telegram.org/bots/features#botfather)  
- `TELEGRAM_USER_ID` - Ваш telegram-ID. Узнать ID можно, например, у этого [бота](https://t.me/username_to_id_bot)   
- `VK_USER_ID` - Ваш VK-ID. [Узнать ID](https://vk.com/faq18062)  
- `VK_TOKEN`- Инструкция по Implicit Flow для получения [ключа доступа пользователя ВК](https://vk.com/dev/implicit_flow_user)  
- `GOOGLE_CLOUD_PROJECT` - ID проекта в Google Cloud (Project ID), привязанноо к DialogFlow [Инструкция, как создать.](https://cloud.google.com/dialogflow/es/docs/quick/setup)    
    [Еще туториал](https://developers.google.com/assistant/df-asdk/dialogflow/project-agent?skip_cache=true%22%22&hl=ru)   


## Установка и настройка
Для запуска у вас уже должен быть установлен Python не ниже 3-й версии.  
В командной строке:  
- Скачайте код: `git clone https://github.com/mulchus/recognize_speech.git`
- Создайте файл с переменными окружения, активируйте виртуальное окружение: 
    `python -m venv venv`  
    - Windows: `.\venv\Scripts\activate`  
    - MacOS/Linux: `source venv/bin/activate`  
- Установите зависимости: `pip install -r requirements.txt`  

#### Внесите в DialogFlow ожидаемые от пользователя вопросы и ответы на них  
- В DialogFlow установите дополнительным [русский язык](https://developers.google.com/assistant/df-asdk/localization?hl=ru)
- В корневой дирректории создайте файл вопросов-ответов `questions.json` в следующем формате (пример):  
```commandline
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
    ...
}
```
- Запустите скрипт `python push_questions.py`

- Запуск бота в Telegram - `python tg.py`  
- Запуск бота в VK - `python vk.py` (в отдельном окне командной строки)  
  
Общайтесь с ботами и наслаждайтесь реакцией. 


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
