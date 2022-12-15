from abc import ABC, abstractmethod

from core.settings import Messages
from db.mongodb.mongodb import AsyncMongoDB
from db.redis import AsyncCacheStorage
from models.like import Like


class BaseSearchService(ABC):

    @abstractmethod
    async def find(self, query: str, **kwargs):
        pass

    @abstractmethod
    async def get_list(self, **kwargs):
        pass

    @abstractmethod
    async def get_details(self, obj_id: str, **kwargs):
        pass


class MongoDBService(BaseSearchService):
    """ Class implements general functionality of data get services. """

    model: Like
    query = None
    errors = []

    def __init__(self, cache: AsyncCacheStorage, source: AsyncMongoDB, mess: Messages):
        """ Init object of BaseService class. """

        self.data_source = source
        self.data_cache = cache
        self.messages = mess

        self.messages.not_found_index = self.messages.not_found_index.format(
            self.model.Config.collection,
            self.model.Config.alias
        )
        self.messages.not_search_result = self.messages.not_search_result.format(
            self.model.Config.alias,
            '{0}',
        )

        self.errors = []

    async def find(self, query: str, **kwargs) -> Like:

        # data = await self.data_source.get_data_by_id(obj_id, kwargs['model'].Config.index)
        # if not data:
        #     self.errors.append(self.messages.not_found_doc.format(kwargs['model'].Config.alias, obj_id))
        #     return None
        # return kwargs['model'](**data)
        pass

    async def get_list(
            self,
            params: dict,
            filters: dict,
            model,
            query: str | None = None
    ) -> list[Like] | None:
        """ Get list of documents according to parameters.

        Arguments:
            query: query string
            params: parameters for search set up
            filters: filters for search
            model: model of objects in list

        Returns:
            list[Like] | None: list of objects or None if list empty
        """

        # self.errors = []
        # self.query = ElasticsearchFieldQuery()
        #
        # source = list(model.schema()['properties'].keys())
        #
        # search_filters = {key: value for key, value in filters.items() if value}
        #
        # if search_filters or query:
        #
        #     for filter_key, filter_value in search_filters.items():
        #         if not await self.filters_methods[filter_key](filter_key, filter_value):
        #             return None
        #
        # if query:
        #     await self.query.append_query_string(query)
        #
        # data = await self.data_source.search(model.Config.index, source, self.query.query, params)
        #
        # if not data:
        #     return None
        #
        # return [model(**doc) for doc in data]
        pass

    @abstractmethod
    async def get_details(self, obj_id: str, **kwargs):
        pass
