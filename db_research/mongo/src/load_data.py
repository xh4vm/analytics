import argparse
import logging
from collections import namedtuple

from adapters.mongo.client import database_client
from core.settings import db_research_settings, mongo_settings
from data_generator.data_generator import DataGenerator
from data_loader.data_loader import DataLoader

logging.basicConfig(level=logging.INFO)


class ArgumentsSetter:
    """ Class for get and set incoming arguments."""
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="""Load data in the collections in the database {0}.
             If no option is specified load all collections.""".format(mongo_settings.DATABASE))
        self.parser.add_argument(
            '-l',
            '--likes',
            action='store_true',
            help='Load data in the collection likes.'
        )
        self.parser.add_argument(
            '-r',
            '--reviews',
            action='store_true',
            help='load data to collections reviews adn reviews_likes.'
        )
        self.parser.add_argument(
            '-b',
            '--bookmarks',
            action='store_true',
            help='Load data in the collection bookmarks.'
        )
        self.parser.add_argument(
            '-s',
            '--seed',
            default=db_research_settings.FAKER_SEED,
            help='Seed for faker.'
        )
        self.arguments = self.parser.parse_args()


def load_data(load_flags: namedtuple, seed):

    load_all_flag = not all(load_flags)

    data_generator = DataGenerator(
        batch_size=db_research_settings.LOAD_BATCH_SIZE,
        seed=seed,
        users_number=db_research_settings.NUMBER_USERS,
        films_number=db_research_settings.NUMBER_FILMS
    )

    data_loader = DataLoader(
        data_generator=data_generator,
        number_likes=db_research_settings.NUMBER_LIKES,
        number_reviews=db_research_settings.NUMBER_REVIEWS,
        number_reviews_likes=db_research_settings.NUMBER_REVIEWS_LIKES,
        number_bookmarks=db_research_settings.NUMBER_BOOKMARKS,
        database_client=database_client,
    )

    data_loader.init()

    if load_all_flag or load_flags.load_likes:
        data_loader.load_likes()

    result_load_reviews = False
    if load_all_flag or load_flags.load_reviews:
        result_load_reviews = data_loader.load_reviews()

    if result_load_reviews:
        data_loader.load_reviews_likes()

    if load_all_flag or load_flags.load_bookmarks:
        data_loader.load_bookmarks()


if __name__ == '__main__':
    args = ArgumentsSetter()
    LoadFlags = namedtuple('LoadFlags', 'load_likes load_reviews load_bookmarks')
    load_all = LoadFlags(args.arguments.likes, args.arguments.reviews, args.arguments.bookmarks)
    seed_arg = args.arguments.seed
    load_data(load_all, args.arguments.seed)
