""" API service for movies. """

import logging

import aioredis
import uvicorn as uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from src.api.v1 import bookmarks, likes, reviews
from src.core.config import SETTINGS
from src.core.logger import LOGGING
from src.db.mongodb.mongodb import mdb
from src.db.redis import redis

app = FastAPI(
    title=SETTINGS.NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    description=SETTINGS.DESCRIPTION,
    version=SETTINGS.VERSION,
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is required')
    return await call_next(request)


@app.on_event('startup')
async def startup():
    """ Execute connects to databases on event startup. """
    redis.cash = aioredis.from_url(**SETTINGS.REDIS.dict())
    redis.expires = SETTINGS.REDIS_EXPIRES
    mdb.cl = AsyncIOMotorClient(SETTINGS.MONGODB.CONNECT_STRING)
    mdb.init_db(SETTINGS.MONGODB.DATABASES['db_data'])


@app.on_event('shutdown')
async def shutdown():
    """ Execute close connects to databases on event shutdown. """
    await redis.cash.close()
    mdb.cl.close()


app.include_router(likes.router, prefix='/api/v1/likes')
app.include_router(reviews.router, prefix='/api/v1/reviews')
app.include_router(bookmarks.router, prefix='/api/v1/bookmarks')


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=SETTINGS.FEEDBACKS_API_PORT,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
