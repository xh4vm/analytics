import json
from collections import OrderedDict
from pathlib import Path

from adapters.mongo.client import MongoBDClient
from core.settings import logger
from utility.utility import DateEncoder, datetime_parser


def perform_command_from_json_file(database_client: MongoBDClient, json_file_full_path: str, save_flag: bool = False):
    json_file_full_path = Path(json_file_full_path)

    if not json_file_full_path.exists():
        logger.error('File {0} does not exist'.format(json_file_full_path))
        return False

    with open(json_file_full_path, 'r') as input_file:
        collections = json.loads(input_file.read(), object_hook=datetime_parser)

    results = {}
    for scope, collection in collections.items():
        result, start_time, time_exec = database_client.exec_command(scope, OrderedDict(collection))
        count = result.get('n')
        if result.get('ok'):
            logger.info('Command {0} start at {1} execute for {2}{3}'.format(
                scope,
                start_time,
                time_exec,
                '. Result count <{0}>.'.format(count) if count else ''
            ))
            results[scope] = result

    if save_flag:
        output_file_name = json_file_full_path.with_name('{0}.txt'.format(json_file_full_path.stem))
        with open(output_file_name, 'w') as output_file:
            json.dump(results, output_file, cls=DateEncoder)
        logger.info('Results off commands save in file {0}'.format(output_file_name))
    return results
