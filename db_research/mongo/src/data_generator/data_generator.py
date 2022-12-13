from itertools import product
from typing import Any

from faker import Faker


class DataGenerator:
    created_ids: list = []

    def __init__(self, batch_size=1, users_number=1, films_number=1, seed=None):

        self.faker_maker = Faker()
        Faker.seed(seed)
        self.batch_size = batch_size
        self.users_ids = [self.faker_maker.uuid4() for _ in range(users_number)]
        self.films_ids = [self.faker_maker.uuid4() for _ in range(films_number)]
        self.objects_couple_ids = {'film_id': Any, 'review_id': Any}

    def set_created_ids(self, data):
        self.created_ids.extend(data)

    def set_objects_couple_ids_review_id(self):
        self.objects_couple_ids['review_id'] = product(self.users_ids, self.created_ids)
        pass

    def set_objects_couple_ids_films_id(self):
        self.objects_couple_ids['film_id'] = product(self.users_ids, self.films_ids)
        pass

    def get_data_unit(self, field_name: str) -> dict:
        created = self.faker_maker.date_time_ad(start_datetime='-3y')
        modified = self.faker_maker.date_time_ad(start_datetime=created)
        user_id, obj_id = next(self.objects_couple_ids[field_name])
        data = {
            'user_id': user_id,
            field_name: obj_id,
            'created': created,
            'modified': modified,
        }
        return data

    def generate_likes(self, field_name: str, count: int) -> list:

        while count > 0:

            likes = []
            batch = self.batch_size if count > self.batch_size else count

            for _ in range(batch):
                like = self.get_data_unit(field_name)
                like['rating'] = self.faker_maker.random.randint(0, 10)
                likes.append(like)

            yield likes
            count -= len(likes)

    def generate_reviews(self, field_name: str, count: int) -> list:

        while count > 0:

            reviews = []
            batch = self.batch_size if count > self.batch_size else count

            for _ in range(batch):
                review = self.get_data_unit(field_name)
                review['text'] = self.faker_maker.text()
                reviews.append(review)

            yield reviews
            count -= len(reviews)

    def generate_bookmarks(self, field_name: str, count: int) -> list:

        while count > 0:
            bookmarks = []
            batch = self.batch_size if count > self.batch_size else count
            for _ in range(batch):
                bookmarks.append(self.get_data_unit(field_name))

            yield bookmarks
            count -= len(bookmarks)
