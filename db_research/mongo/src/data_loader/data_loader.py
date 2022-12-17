from dataclasses import dataclass
from datetime import timedelta

from adapters.mongo.client import MongoBDClient
from core.settings import logger
from data_generator.data_generator import DataGenerator


@dataclass
class DataLoader:
    """ Class to load data """

    data_generator: DataGenerator = None
    number_likes: int = 1
    number_reviews: int = 1
    number_reviews_likes: int = 1
    number_bookmarks: int = 1
    database_client: MongoBDClient = None
    options: dict = None

    def init(self):
        self.options = {
            'likes': {
                'generate_objects_couples': self.data_generator.set_objects_couple_ids_films_id,
                'collection_generator': self.data_generator.generate_likes,
                'number_docs': self.number_likes,
                'field_name': 'film_id',
            },
            'reviews': {
                'generate_objects_couples': self.data_generator.set_objects_couple_ids_films_id,
                'collection_generator': self.data_generator.generate_reviews,
                'number_docs': self.number_reviews,
                'field_name': 'film_id',
            },
            'reviews_likes': {
                'generate_objects_couples': self.data_generator.set_objects_couple_ids_review_id,
                'collection_generator': self.data_generator.generate_likes,
                'number_docs': self.number_reviews_likes,
                'field_name': 'review_id',
                'addition': None,
            },
            'bookmarks': {
                'generate_objects_couples': self.data_generator.set_objects_couple_ids_films_id,
                'collection_generator': self.data_generator.generate_bookmarks,
                'number_docs': self.number_bookmarks,
                'field_name': 'film_id',
            },
        }

    def load_base(self, collection: str) -> bool:
        """ Common function for load data.

        Arguments:
            collection: name of collection for load.
        Returns:
            bool: result
        """

        all_time_exec = timedelta(0)
        self.options[collection]['generate_objects_couples']()
        collection_generator = self.options[collection]['collection_generator'](
            field_name=self.options[collection]['field_name'],
            count=self.number_likes,
        )
        counter = 0
        for collection_batch in collection_generator:
            result, start_time, time_exec = self.database_client.insert_many(collection, collection_batch)
            if not result.acknowledged:
                logger.error('Вставка данных в коллекцию <{0}> не подтверждена'.format(collection))
                return False
            counter += len(result.inserted_ids)
            logger.info('<{0}>. Добавлено документов {1} из {2}'.format(collection, counter, self.number_likes))
            self.data_generator.created_ids.extend(result.inserted_ids)
            all_time_exec += time_exec

        logger.info('<{0}>. Время загрузки данных: {1}'.format(collection, all_time_exec))

        return True

    def load_likes(self):
        return self.load_base('likes')

    def load_reviews(self):
        return self.load_base('reviews')

    def load_reviews_likes(self):
        return self.load_base('reviews_likes')

    def load_bookmarks(self):
        return self.load_base('bookmarks')
