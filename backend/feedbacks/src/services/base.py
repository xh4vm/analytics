from abc import ABC, abstractmethod
from datetime import datetime
from http import HTTPStatus

from pymongo.errors import DuplicateKeyError
from src.core.config import SETTINGS
from src.core.settings import Messages
from src.db.mongodb.mongodb import AsyncMongoDB
from src.db.redis import AsyncCacheStorage


class BaseSearchService(ABC):

    @abstractmethod
    async def create_doc(self, params: dict, **kwargs):
        pass

    @abstractmethod
    async def update_doc(self, find: dict, update: dict, **kwargs):
        pass

    @abstractmethod
    async def delete_doc(self, params: dict, **kwargs):
        pass

    @abstractmethod
    async def get_doc_avg_rating(self, data: dict):
        pass


class MongoDBService(BaseSearchService):
    """ Class implements general functionality of data get services. """

    model: None
    query = None
    errors = None

    def __init__(self, cache: AsyncCacheStorage, source: AsyncMongoDB, mess: Messages):
        """ Init object of BaseService class. """

        self.data_source = source
        self.data_cache = cache
        self.messages = mess

        self.errors = {}

    async def create_doc(self, params: dict, **kwargs):
        current_model = kwargs.get('model', self.model)
        doc = {**params, 'created': datetime.utcnow(), 'modified': datetime.utcnow()}
        err, result = await self.data_source.insert_one(current_model.Config.collection, doc)
        if isinstance(err, DuplicateKeyError):
            self.errors = {'status': HTTPStatus.CONFLICT, 'message': err.args[0]}
            return None
        return current_model.parse_obj({**doc, 'id': str(result.inserted_id)})

    async def update_doc(self, find: dict, update: dict, **kwargs):

        update = {**update, 'modified': datetime.utcnow()}
        query_update = {'$set': update}

        result = await self.data_source.update_one(self.model.Config.collection, find, query_update)
        return result if not result else self.model.parse_obj(result)

    async def delete_doc(self, params: dict, **kwargs):

        delete_review = await self.data_source.delete_one(self.model.Config.collection, params)

        return delete_review

    async def get_doc_avg_rating(self, data: dict):
        match = {'$match': data}
        group = {
            '$group': {
                '_id': None,
                'avg_val': {'$avg': '$rating'}
            }
        }
        result = await self.data_source.aggregate(self.model.Config.collection, match, group)
        return result[0] if result else None

    async def get_number_doc_likes(self, field_name: str, field_value: str, **kwargs):
        current_model = kwargs.get('model', self.model)
        query = {
            '$and': [
                {field_name: {'$eq': field_value}},
                {'rating': None}
            ]
        }
        query['$and'][1]['rating'] = SETTINGS.MONGODB.LIKES
        number_likes = await self.data_source.count('likes', query)

        query['$and'][1]['rating'] = SETTINGS.MONGODB.DISLIKE
        number_dislikes = await self.data_source.count('likes', query)

        result = current_model.parse_obj(
            {field_name: field_value, 'number_likes': number_likes, 'number_dislikes': number_dislikes}
        )
        return result

    async def get_doc_list(self, **kwargs):
        result = await self.data_source.find(collection=self.model.Config.collection, query=kwargs)
        return result
