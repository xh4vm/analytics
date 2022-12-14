from functools import lru_cache

from fastapi import Depends
from src.core.config import get_messages
from src.core.settings import Messages
from src.db.mongodb.mongodb import AsyncMongoDB, get_mongodb
from src.db.redis import AsyncCacheStorage, get_redis
from src.models.bookmarks import Bookmark
from src.services.base import MongoDBService


class BookmarkService(MongoDBService):

    model = Bookmark


@lru_cache()
def get_bookmark_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        db_storage_source: AsyncMongoDB = Depends(get_mongodb),
        messages: Messages = Depends(get_messages,),
) -> BookmarkService:
    """ Get BookmarksService object.

    Arguments:
        cache: class for work with redis
        db_storage_source: class for work with mongodb
        messages: messages

    Returns:
        BookmarkService: bookmark service
    """

    messages.list_empty = messages.list_empty.format('bookmarks')

    return BookmarkService(cache, db_storage_source, messages)
