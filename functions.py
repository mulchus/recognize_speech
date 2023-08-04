import os
import logging
import telegram

from google.cloud import dialogflow
from dotenv import load_dotenv


class CustomLogsHandler(logging.Handler):
    def __init__(self, bot, user_id):
        super().__init__()
        self.bot = bot
        self.user_id = user_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(self.user_id, log_entry)


def set_logger():
    logger = logging.getLogger("event_logging")
    load_dotenv()
    tg_controlbot = telegram.Bot(os.environ.get('TELEGRAM_CONTROLBOT_TOKEN'))
    tg_user_id = os.environ.get('TELEGRAM_USER_ID')
    logger.setLevel(logging.INFO)
    logger_settings = CustomLogsHandler(tg_controlbot, tg_user_id)
    logger_settings.setLevel(logging.INFO)
    logger_settings.setFormatter(logging.Formatter("%(asctime)s: %(levelname)s; %(message)s",
                                                   datefmt="%d/%b/%Y %H:%M:%S"))
    logger.addHandler(logger_settings)
    return logger


def detect_intent_text(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    intent_text = response.query_result.fulfillment_text
    is_fallback = response.query_result.intent.is_fallback
    return intent_text, is_fallback
