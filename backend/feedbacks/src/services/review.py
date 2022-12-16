from functools import lru_cache

from bson import ObjectId
from core.config import get_messages
from core.settings import Messages
from db.mongodb.mongodb import AsyncMongoDB, get_mongodb
from db.redis import AsyncCacheStorage, get_redis
from fastapi import Depends
from models.review import Review
from services.base import MongoDBService


class ReviewService(MongoDBService):

    model = Review

    async def update_review(self, params: dict, **kwargs):
        like_find = {
            'user_id': params.get('user_id'),
            'film_id': params.get('film_id'),
        }
        like_update = {
            'text': params.get('text'),
        }

        result = await self.update_doc(like_find, like_update)
        return result if not result else Review.parse_obj(result)

    async def create_review_like(self, params: dict, **kwargs):
        params['review_id'] = ObjectId(params['review_id'])
        return await self.create_doc(params, **kwargs)

    def format_command(self):
        lookup = {
            '$lookup':
                {
                    'from': self.model.Config.collection_likes,
                    'localField': '_id',
                    'foreignField': 'review_id',
                    'as': 'r_likes',
                    'pipeline': [
                        {
                            "$group": {
                                "_id": "$review_id",
                                "avg_rating": {"$avg": "$rating"}
                            }
                        }
                    ]
                }
        }
        project = {
            '$project':
                {
                    '_id': 1,
                    'film_id': 1,
                    'user_id': 1,
                    'text': 1,
                    'created': 1,
                    'modified': 1,
                    'r_likes.avg_rating': 1,
                    'avg_rating': {'$first': '$r_likes.avg_rating'},
                }
        }

        return lookup, project

    async def get_reviews_list(self, **kwargs):

        # if not kwargs['filter_likes']:
        #     return await self.data_source.find(
        #         self.model.Config.collection,
        #         query=kwargs['filters'],
        #         options=kwargs['params'],
        #     )

        lookup, project = self.format_command()

        match = None
        if kwargs['filters'] or kwargs['filters_likes']:
            match = {'$match': {}}

        if kwargs['filters']:
            match['$match'].update(kwargs['filters'])

        if kwargs['filters_likes']:
            match['$match'].update({'r_likes.avg_rating': kwargs['filters_likes']})

        result = await self.data_source.aggregate(
            collection=self.model.Config.collection,
            lookup=lookup,
            project=project,
            match=match,
            limit={'$limit': kwargs['params'].limit},
            skip={'$skip': kwargs['params'].skip},
        )
        return result


@lru_cache()
def get_review_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        db_storage_source: AsyncMongoDB = Depends(get_mongodb),
        messages: Messages = Depends(get_messages,),
) -> ReviewService:
    """ Get ReviewService object.

    Arguments:
        cache: class for work with redis
        db_storage_source: class for work with mongodb
        messages: messages

    Returns:
        PersonService: like service
    """

    messages.list_empty = messages.list_empty.format('likes')

    return ReviewService(cache, db_storage_source, messages)
