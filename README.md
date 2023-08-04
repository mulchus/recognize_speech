# Боты распознавания речи в Telegram и VK


## Переменные окружения
Часть настроек проекта берётся из переменных окружения.  
Чтобы их определить, создайте файл `.env` в корневой папке `recognize_speech` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`:    
- `TELEGRAM_BOT_TOKEN` - токен основного бота Телеграмм. [Инструкция, как создать бота.](https://core.telegram.org/bots/features#botfather)  
- `TELEGRAM_CONTROLBOT_TOKEN`- токен контрольного бота Телеграмм, отсылающего Вам сообщения об ошибках.  
- `TELEGRAM_USER_ID` - Ваш telegram-ID. Узнать ID можно, например, у этого [бота](https://t.me/username_to_id_bot)
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
- В корневой дирректории создайте файл вопросов-ответов (по умолчанию - `questions.json`) в следующем формате JSON (пример):  
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
- Запустите скрипт `python push_questions.py [имя_файла.json]`
- Выборочно проверьте, что в DialogFlow правильно загрузились все вопросы-ответы для вкладки 'ru' возле имени проекта.  

- Запуск бота в Telegram - `python tg.py`  
- Запуск бота в VK - `python vk.py` (в отдельном окне командной строки)

  Результат общения с [ботом в Telegram](https://t.me/mulchusbot)  
  ![tg](https://github.com/mulchus/recognize_speech/assets/111083714/4dd30098-b266-42a0-9db2-79eb08250066)
  
  Результат общения с [ботом в VK](https://vk.com/club219033181)  
  ![vk](https://github.com/mulchus/recognize_speech/assets/111083714/58b30366-44e9-421f-85a6-43ba0057ed22)
  
Общайтесь с ботами и наслаждайтесь реакцией. 


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
