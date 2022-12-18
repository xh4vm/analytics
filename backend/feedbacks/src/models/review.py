""" Model Review. """

from bson import ObjectId
from pydantic import Field, validator

from .base import BaseMixin, DateMixin, PyObjectId


class Review(BaseMixin, DateMixin):
    """ Class for Film review model. """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    film_id: str
    text: str = Field('Text film review', max_length=1000)

    class Config:
        collection = 'reviews'
        collection_likes = 'reviews_likes'
        alias = 'Reviews'
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @validator('id')
    def replace_none_to_list(cls, v):
        return str(v)


class ReviewLike(BaseMixin, DateMixin):
    """ Class for Review like model. """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = None
    review_id: PyObjectId = Field(default_factory=PyObjectId)
    rating: int = None

    class Config:
        collection = 'reviews_likes'
        alias = 'Review Like'
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @validator('id')
    def replace_none_to_list(cls, v):
        return str(v)


class ReviewAvgRating(Review):
    """ Class for Film review model with average. """

    avg_rating: float = None


class ReviewDeleteLikes(Review):
    """ Class for Film review model with deleted likes count. """

    deleted_likes_count: int = None
