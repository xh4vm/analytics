""" Class and functions for work with radis."""

from abc import ABC, abstractmethod
from functools import wraps

from aioredis import Redis
from src.api.v1.utilitys import test_connection
from src.models.base import get_obj, get_str


class AsyncCacheStorage(ABC):

    @abstractmethod
    async def get_from_cache(self, key: str, **kwargs):
        pass

    @abstractmethod
    async def set_to_cache(self, key: str, value, expire: int, **kwargs):
        pass


class RedisCache(AsyncCacheStorage):
    """ Class for redis cash service. """

    def __init__(self):
        """ Init RedisCash"""
        self.cash: Redis | None = None
        self.expires: int | None = None

    @test_connection
    async def set_to_cache(self, key, value, **kwargs):
        """ Set data to redis cash."""
        await self.cash.set(key, value, ex=self.expires)

    @test_connection
    async def get_from_cache(self, key, **kwargs):
        """ Get data from redis cash."""

        return await self.cash.get(key)


redis = RedisCache()


async def get_redis() -> RedisCache:
    """ Get redis object. """

    return redis


def use_cache(model):
    """ Set parameter to decorator.

     Arguments:
        model: model
    """
    def cache_decorator(func):
        """ Decorator for redis cash.
        The wrapped function must have arguments request and obj_service.
        """

        @wraps(func)
        async def wrapper(*args, **kwargs):
            """ A wrapper for a function whose execution result is subject to caching.

            Arguments:
                args: positional arguments
                kwargs: keyword arguments, must have
                    kwargs['obj_service'] - object service whose work result is subject to caching
                    kwargs['request'] - query parameters
            """
            cache_driver = kwargs['obj_service'].data_cache
            key = await create_key(kwargs['request'])
            result = await get_obj(model, await cache_driver.get_from_cache(key))
            if result is None:
                result = await func(*args, **kwargs)
                await cache_driver.set_to_cache(key, await get_str(result))
            return result

        async def create_key(params):
            """ Create key for parameters. """

            query_params_part = '-'.join(['-'.join(q) for q in sorted(params.query_params.items())])
            key_parts = [func.__name__, params.url.path, query_params_part]
            key = '-'.join(key_parts)
            return key

        return wrapper
    return cache_decorator
