from functools import wraps
from http import HTTPStatus

import backoff
from aiohttp.client_exceptions import ClientConnectorError
from aioredis.exceptions import ConnectionError
from core.config import SETTINGS
from fastapi import HTTPException


async def check_result(result, errors: list, messages):
    if not result:
        details = '{0} {1}'.format(messages, '\n'.join(errors))
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=details.strip()
        )


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
        (ConnectionError, ClientConnectorError),
        max_tries=SETTINGS.BACKOFF_MAX_TRIES,
        on_giveup=fatal_error,
    )
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    return wrapper
