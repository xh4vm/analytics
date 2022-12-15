from pathlib import Path

from pydantic import BaseModel, BaseSettings

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent


class RedisS(BaseSettings):
    """Class settings for Redis."""

    url: str
    port: int
    encoding: str = "utf-8"
    decode_responses: bool = True
    max_connections: int = 20

    class Config:
        env_prefix = 'REDIS_'
        env_file = Path(ROOT_DIR, '.env')


class MongoSettings(BaseSettings):
    CONNECT_STRING: str
    DATABASES: dict
    LIKES = {'$eq': 10}
    DISLIKE = {'$eq': 0}

    class Config:
        env_prefix = 'MONGO_'
        env_file = Path(ROOT_DIR, '.env')
        env_file_encoding = "utf-8"


class Settings(BaseSettings):
    """Class main settings."""

    REDIS = RedisS().parse_obj(RedisS().dict())
    MONGODB = MongoSettings().parse_obj(MongoSettings().dict())
    NAME: str
    DESCRIPTION: str
    VERSION: str
    REDIS_EXPIRES: int = 300
    BACKOFF_MAX_TRIES: int = 3
    CREATE_COLLECTIONS_COMMANDS_JSON_FILE: str = ""
    CREATE_COLLECTIONS_INDEXES_COMMANDS_JSON_FILE: str = ""

    class Config:
        env_prefix = 'PROJECT_'
        env_file = Path(ROOT_DIR, '.env')


class Messages(BaseModel):
    """ Class for setup message fot service. """

    list_empty: str = 'List of {0} is empty'
    not_found_index: str = 'Not found index {0} for model {1}.'
    not_found_doc: str = '{0} with ID {1} not found.'
    not_search_result: str = 'Documents of model {0} according to query string <{1}> not found.'

    def __hash__(self):
        return hash(self.json())
