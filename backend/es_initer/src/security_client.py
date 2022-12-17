import backoff
from config.base import BACKOFF_CONFIG
from config.logger import logger
from elasticsearch import Elasticsearch
from elasticsearch.client import SecurityClient
from elastic_transport import ObjectApiResponse


class SecurityClientElasticsearch:
    def __init__(self, conn: Elasticsearch = None) -> None:
        self._security_client: SecurityClient = SecurityClient(client=conn)

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def change_password(self, username: str, password: str) -> ObjectApiResponse:
        return self._security_client.change_password(username=username, password=password)
