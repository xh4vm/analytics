import datetime
from functools import lru_cache

from api.v1.params import FilmUserIDsParams
from core.config import SETTINGS, get_messages
from core.settings import Messages
from db.mongodb.mongodb import AsyncMongoDB, get_mongodb
from db.redis import AsyncCacheStorage, get_redis
from fastapi import Depends
from models.like import FilmsLikes, Like
from services.base import MongoDBService


class LikeService(MongoDBService):

    model = Like

    async def get_films_likes(self, film_id: str):
        query = {
            '$and': [
                {'film_id': {'$eq': film_id}},
                {'rating': None}
            ]
        }
        query['$and'][1]['rating'] = SETTINGS.MONGODB.LIKES
        number_likes = await self.data_source.count('likes', query)

        query['$and'][1]['rating'] = SETTINGS.MONGODB.DISLIKE
        number_dislikes = await self.data_source.count('likes', query)

        return FilmsLikes(id_film=film_id, number_likes=number_likes, number_dislikes=number_dislikes)

    async def create_like(self, params: FilmUserIDsParams, rating: int, **kwargs):
        like = Like(
            user_id=str(params.user_id),
            film_id=str(params.film_id),
            rating=rating,
            created=datetime.datetime.utcnow(),
            modified=datetime.datetime.utcnow(),
        )
        result = await self.data_source.insert_one('likes', like.dict())
        like.id = str(result.inserted_id)
        return like

    async def get_details(self, obj_id: str, **kwargs):
        pass


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
        PersonService: like service
    """

    messages.list_empty = messages.list_empty.format('likes')

    return LikeService(cache, db_storage_source, messages)
