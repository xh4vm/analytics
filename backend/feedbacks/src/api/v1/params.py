# General classes for routers
import random
import uuid

from fastapi import Body, Query
from src.models.base import PyObjectId
from pydantic.types import UUID4
from src.utility.utility import str_if_uuid


class MixinParams:
    def get_dict(self):
        return {
            params_key: str_if_uuid(params_value) for params_key, params_value in self.__dict__.items() if params_value
        }


class FilmUserIDsParams(MixinParams):
    """ Class provide film and user ids query parameters."""
    def __init__(
        self,
        film_id: UUID4 = Body(description="ID of film", default=uuid.uuid4()),
        user_id: UUID4 = Body(description="ID of user", default=uuid.uuid4())
    ):
        self.film_id = film_id
        self.user_id = user_id


class ReviewUserIDsParams(MixinParams):
    """ Class provide review and user ids query parameters"""
    def __init__(
        self,
        review_id: PyObjectId = Body(description="ID of review", default=str(PyObjectId())),
        user_id: UUID4 = Body(description="ID of user", default=uuid.uuid4())
    ):
        self.review_id = review_id
        self.user_id = user_id


class RatingParams:
    """ Class general query parameters."""
    def __init__(
        self,
        rating: int = Body(qe=0, le=10, default=random.randint(0, 10)),
    ):
        self.rating = rating


class CustomQueryParams(MixinParams):
    """ Class general query parameters."""
    def __init__(
        self,
        limit: int = Query(
            ge=1,
            default=10,
            description="""Maximum number of documents to return. If you do not specify this parameter,
            the default limit will be used: 10 documents.""",
        ),
        skip: int = Query(
            ge=0,
            default=0,
            description='Defines the number of documents to skip',
        ),
    ):
        self.limit = limit
        self.skip = skip


class CustomReviewsParams(MixinParams):
    """ Class for parameters for Reviews service. """

    def __init__(
            self,
            film_id: UUID4 = Query(None, description='film_id: UUID', alias='filter_film_id'),
            user_id: UUID4 = Query(None, description='user_id: UUID', alias='filter_user_id'),
     ):
        self.film_id = film_id
        self.user_id = user_id


class CustomReviewsLikesParams(MixinParams):
    """ Class for parameters for likes reviews service. """

    def __init__(
            self,
            gte: float = Query(
                None,
                ge=0,
                le=10,
                description='min average review\'rating',
                alias='filter_min_avg_rating',
            ),
            lte: float = Query(
                None,
                ge=0,
                le=10,
                description='max average review\'rating',
                alias='filter_max_avg_rating',
            ),
    ):
        self.gte = gte
        self.lte = lte

    def get_dict(self):
        return {
            '${0}'.format(params_key): params_value for params_key, params_value in self.__dict__.items() if
            params_value
        }
