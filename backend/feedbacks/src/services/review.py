from functools import lru_cache

from bson import ObjectId
from fastapi import Depends
from src.core.config import get_messages
from src.core.settings import Messages
from src.db.mongodb.mongodb import AsyncMongoDB, get_mongodb
from src.db.redis import AsyncCacheStorage, get_redis
from src.models.review import Review
from src.services.base import MongoDBService


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

    async def delete_review(self, params: dict, **kwargs):
        current_model = kwargs.get('model') or self.model
        deleted_review = await self.delete_doc(params)

        if not deleted_review:
            return None

        result = await self.data_source.delete_many(
            self.model.Config.collection_likes,
            {'review_id': deleted_review['_id']}
        )
        deleted_likes_count = result.deleted_count if result.acknowledged else None

        return current_model(**deleted_review, deleted_likes_count=deleted_likes_count)


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
        ReviewService: review service
    """

    messages.list_empty = messages.list_empty.format('reviews')

    return ReviewService(cache, db_storage_source, messages)
