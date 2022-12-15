""" Model Like. """
from datetime import datetime

from .base import BaseMixin


class Like(BaseMixin):
    """ Class for Film model. """

    id: str = None
    user_id: str
    film_id: str
    rating: int
    created: datetime
    modified: datetime

    class Config:
        collection = 'movies'
        alias = 'Like'


class FilmsLikes(BaseMixin):

    id_film: str
    number_likes: int
    number_dislikes: int

    class Config:
        collection = 'movies'
        alias = 'Like'
