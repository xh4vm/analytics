import logging

logging.basicConfig(
    filename="/var/log/elasticsearch-initer/log.txt",
    filemode='a',
    level=logging.INFO, 
    format='%(asctime)s %(levelname)s %(name)s %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger('ES-INITER')
