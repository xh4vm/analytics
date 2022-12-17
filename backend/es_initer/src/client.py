from typing import Any, Optional

import backoff
from config.base import BACKOFF_CONFIG, ElasticsearchSettings
from config.logger import logger
from elasticsearch import Elasticsearch


def es_conn_is_alive(es_conn: Elasticsearch) -> bool:
    """Функция для проверки работоспособности Elasticsearch"""
    try:
        return es_conn.ping()
    except Exception:
        return False


class ElasticClient:
    def __init__(
        self,
        settings: ElasticsearchSettings,
        username: Optional[str] = None,
        password: Optional[str] = None,
        conn: Optional[Elasticsearch] = None
    ) -> None:
        self._conn: Elasticsearch = conn
        self._username = username
        self._password = password
        self._settings: ElasticsearchSettings = settings

    @property
    def conn(self) -> Elasticsearch:
        if self._conn is None or not es_conn_is_alive(self._conn):
            self._conn = self._reconnection()

        return self._conn

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def _reconnection(self) -> Elasticsearch:
        logger.info('Reconnection elasticsearch...')

        if self._conn is not None:
            logger.info('Closing already exists es connector...')
            self._conn.close()

        return Elasticsearch(
            [
                f'{self._settings.PROTOCOL}://{self._settings.HOST}:{self._settings.PORT}'
            ],
            http_auth=(self._username or self._settings.USER,  self._password or self._settings.PASSWORD)
        )

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def create(self, index_name: str, mapping: dict[str, Any]):
        pass