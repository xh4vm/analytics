""" Model Like. """

from datetime import datetime

from bson import ObjectId
from pydantic import Field, validator

from .base import BaseMixin, PyObjectId


class Like(BaseMixin):
    """ Class for Film like model. """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = None
    film_id: str = None
    rating: int = None
    created: datetime = None
    modified: datetime = None

    class Config:
        collection = 'likes'
        alias = 'Like'
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @validator('id')
    def replace_none_to_list(cls, v):
        return str(v)


class FilmsLikes(BaseMixin):

    film_id: str
    number_likes: int
    number_dislikes: int

    class Config:
        collection = 'likes'
        alias = 'FilmsLikes'


class FilmsAvgRating(BaseMixin):

    film_id: str
    avg_rating: float

    class Config:
        collection = 'likes'
        alias = 'FilmsAvgRating'
