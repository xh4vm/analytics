from functools import lru_cache
from logging import config as logging_config

from core.logger import LOGGING
from core.settings import Messages, Settings

logging_config.dictConfig(LOGGING)


async def get_messages():
    return Messages()


@lru_cache()
def get_settings():
    return Settings()


SETTINGS = get_settings()
