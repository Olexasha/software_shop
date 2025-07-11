import logging
import os

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TG_BOT_TOKEN")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "software_shop.software_shop.settings"
)
