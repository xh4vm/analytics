import os
from pathlib import Path

from loguru import logger
from pydantic import BaseSettings

logger.add(
    'db_research.log',
    format="<g>{time}</g> | <ly>{level}</ly> | <ly>{message}</ly>"
)

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent


class DBResearchSettings(BaseSettings):
    JSON_BENCHMARKS_COMMANDS_PATH: str = ""
    JSON_SCHEMAS_PATH: str
    JSON_INDEXES_PATH: str
    LOAD_BATCH_SIZE: int = 2
    NUMBER_FILMS: int = 2000
    NUMBER_USERS: int = 5000
    NUMBER_LIKES: int = 10
    NUMBER_REVIEWS: int = 5
    NUMBER_REVIEWS_LIKES: int = 10
    NUMBER_BOOKMARKS: int = 10
    FAKER_SEED: int = 314

    class Config:
        env_prefix = 'DB_RESEARCH_'
        env_file = os.path.join(ROOT_DIR, ".env")
        env_file_encoding = "utf-8"


class MongoSettings(BaseSettings):
    CONNECT_STRING: str
    DATABASE: str

    class Config:
        env_prefix = 'MONGO_'
        env_file = os.path.join(ROOT_DIR, ".env")
        env_file_encoding = "utf-8"


mongo_settings = MongoSettings()
db_research_settings = DBResearchSettings()
