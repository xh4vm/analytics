from functools import lru_cache

from fastapi import Depends
from src.core.config import get_messages
from src.core.settings import Messages
from src.db.mongodb.mongodb import AsyncMongoDB, get_mongodb
from src.db.redis import AsyncCacheStorage, get_redis
from src.models.like import FilmsAvgRating, Like
from src.services.base import MongoDBService


class LikeService(MongoDBService):

    model = Like

    async def get_film_avg_rating(self, film_id: str):
        result = await self.get_doc_avg_rating({'film_id': film_id})
        return FilmsAvgRating(film_id=film_id, avg_rating=round(result['avg_val'], 2)) if result else None

    async def update_like(self, params: dict, **kwargs):
        like_find = {
            'user_id': params.get('user_id'),
            'film_id': params.get('film_id'),
        }
        like_update = {
            'rating': params.get('rating'),
        }

        result = await self.update_doc(like_find, like_update)
        return result if not result else Like.parse_obj(result)


@lru_cache()
def get_like_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        db_storage_source: AsyncMongoDB = Depends(get_mongodb),
        messages: Messages = Depends(get_messages,),
) -> LikeService:
    """ Get LikeService object.

    Arguments:
        cache: class for work with redis
        db_storage_source: class for work with mongodb
        messages: messages

    Returns:
        LikeService: like service
    """

    messages.src.list_empty = messages.list_empty.format('likes')

    return LikeService(cache, db_storage_source, messages)
