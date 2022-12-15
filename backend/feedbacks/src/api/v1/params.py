# General classes for routers
import random
import uuid

from fastapi import Body
from pydantic.types import UUID4


class FilmUserIDsParams:
    """ Class general query parameters."""
    def __init__(
        self,
        film_id: UUID4 = Body(description="ID of film", default=uuid.uuid4()),
        user_id: UUID4 = Body(description="ID of user", default=uuid.uuid4())
    ):
        self.film_id = film_id
        self.user_id = user_id

    def get_dict(self):
        return {params_key: str(params_value) for params_key, params_value in self.__dict__.items()}


class RatingParams:
    """ Class general query parameters."""
    def __init__(
        self,
        rating: int = Body(qe=0, le=10, default=random.randint(0, 10)),
    ):
        self.rating = rating
