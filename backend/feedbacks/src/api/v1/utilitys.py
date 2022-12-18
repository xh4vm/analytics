from functools import wraps
from http import HTTPStatus

import backoff
from aiohttp.client_exceptions import ClientConnectorError
from aioredis.exceptions import ConnectionError
from fastapi import HTTPException
from pymongo.errors import ServerSelectionTimeoutError
from src.core.config import SETTINGS


async def check_result(result, errors: dict, messages):
    if errors:
        raise HTTPException(status_code=errors['status'], detail=errors['message'])
    if not result and not errors:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages)


def fatal_error(err):
    raise HTTPException(
            status_code=HTTPStatus.GATEWAY_TIMEOUT,
            detail='The external service for API Service ({0}) is not available now'.format(
                type(err['args'][0]).__name__
            ),
    )


def test_connection(func):
    @backoff.on_exception(
        backoff.expo,
        (ConnectionError, ClientConnectorError, ServerSelectionTimeoutError),
        max_tries=SETTINGS.BACKOFF_MAX_TRIES,
        on_giveup=fatal_error,
    )
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    return wrapper
