import logging
from pathlib import Path
from typing import Any

import backoff
from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent.parent


class AuthSettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_DECODE_ALGORITHMS: list[str]
    JWT_ALGORITHM: str
    JWT_HEADER_NAME: str
    JWT_TOKEN_LOCATION: str = Field('headers')

    class Config:
        env_prefix = 'AUTH_'
        env_file = Path(ROOT_DIR, '.env')


class GRPCSettings(BaseSettings):
    HOST: str
    PORT: int

    class Config:
        env_prefix = 'AUTH_GRPC_'
        env_file = Path(ROOT_DIR, '.env')


class Config(BaseSettings):
    APP: AuthSettings = AuthSettings()
    GRPC: GRPCSettings = GRPCSettings()


CONFIG = Config()
BACKOFF_CONFIG: dict[str, Any] = {'wait_gen': backoff.expo, 'max_value': 128}

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
)
auth_logger = logging.getLogger(name='Auth Client')
