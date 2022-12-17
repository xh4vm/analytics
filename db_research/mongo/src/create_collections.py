import argparse
from os import path

from adapters.mongo.client import database_client
from commands.commands_utility import perform_command_from_json_file
from core.settings import (ROOT_DIR, db_research_settings, logger,
                           mongo_settings)


class ArgumentsSetter:
    """ Class for get and set incoming arguments."""
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Created collections in the database {0}'.format(mongo_settings.DATABASE),
        )
        self.parser.add_argument(
            '-i',
            '--index',
            action='store_true',
            help='Create indexes. !!! Collections must be already created !!!'
        )
        self.parser.add_argument(
            '-d',
            '--drop',
            action='store_true',
            help='Drop all collections before create.'
        )
        self.arguments = self.parser.parse_args()


def create_collections(index_flag: bool, drop_flag: bool) -> bool:
    """ Create collections

    Arguments:
        index_flag: if set only collection's indexes will be created
        drop_flag: if set  collection wil be removed before created
    Returns:
        bool: result
    """

    if drop_flag:
        database_client.drop_collection()
        logger.info('All collections in the database {0} have been deleted.')

    if index_flag:
        json_schema_full_path = path.join(ROOT_DIR, db_research_settings.JSON_INDEXES_PATH)
    else:
        json_schema_full_path = path.join(ROOT_DIR, db_research_settings.JSON_SCHEMAS_PATH)

    perform_command_from_json_file(database_client, json_schema_full_path)


if __name__ == '__main__':
    create_indexes = ArgumentsSetter().arguments.index
    drop_collections_flag = ArgumentsSetter().arguments.drop
    create_collections(create_indexes, drop_collections_flag)
