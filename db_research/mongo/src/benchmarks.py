import argparse
from os import path

from adapters.mongo.client import database_client
from commands.commands_utility import perform_command_from_json_file
from core.settings import ROOT_DIR, db_research_settings
from data_generator.data_generator import DataGenerator
from data_loader.data_loader import DataLoader


class ArgumentsSetter:
    """ Class for get and set incoming arguments."""
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Perform commands from file {0}'.format(db_research_settings.JSON_BENCHMARKS_COMMANDS_PATH),
        )
        self.parser.add_argument(
            '-s',
            '--save',
            action='store_true',
            help='Save the result of performing commands to a file.'
        )
        self.arguments = self.parser.parse_args()


def insert_one_document_in_collection():

    data_generator = DataGenerator()
    data_loader = DataLoader(data_generator=data_generator, database_client=database_client)

    data_loader.init()

    data_loader.load_likes()

    result_load_reviews = data_loader.load_reviews()
    if result_load_reviews:
        data_loader.load_reviews_likes()

    data_loader.load_bookmarks()


def run_query(flag_save_results):

    insert_one_document_in_collection()

    perform_command_from_json_file(
        database_client,
        path.join(ROOT_DIR, db_research_settings.JSON_BENCHMARKS_COMMANDS_PATH),
        save_flag=flag_save_results,
    )


if __name__ == '__main__':
    save_flag = ArgumentsSetter().arguments.save
    run_query(save_flag)
