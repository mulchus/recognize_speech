import logging
import os
from dotenv import load_dotenv


load_dotenv()
telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_user_id = os.getenv('TELEGRAM_USER_ID')
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
vk_token = os.getenv('VK_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    pass


if __name__ == '__main__':
    main()
