from elasticsearch import AuthenticationException

from config.base import ELASTIC_CONFIG, SECURITY_DEFAULT_ELASTIC_CONFIG, SECURITY_CONFIG
from client import ElasticClient
from security_client import SecurityClientElasticsearch

if __name__ == '__main__':
    es_client = None
    try:
        es_client = ElasticClient(
            settings=ELASTIC_CONFIG,
            username=ELASTIC_CONFIG.USER,
            password=ELASTIC_CONFIG.PASSWORD
        )
        es_client.conn.info()
    except AuthenticationException:
        es_client = ElasticClient(
            settings=ELASTIC_CONFIG,
            username=SECURITY_DEFAULT_ELASTIC_CONFIG.USER,
            password=SECURITY_DEFAULT_ELASTIC_CONFIG.PASSWORD
        )
        es_client.conn.info()

    security_client = SecurityClientElasticsearch(conn=es_client.conn)

    for config in SECURITY_CONFIG:
        security_client.change_password(username=config.USER, password=config.PASSWORD)
