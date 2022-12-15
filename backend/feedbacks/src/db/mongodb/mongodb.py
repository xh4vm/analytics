from abc import ABC, abstractmethod

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class AsyncDBStorage(ABC):

    @abstractmethod
    async def exec_command(self, db_name: str, command: dict, *args, **kwargs):
        pass

    @abstractmethod
    async def insert_one(self, collection: str, data: dict,  *args, **kwargs):
        pass

    @abstractmethod
    async def update_one(self, collection: str, data: dict, *args, **kwargs):
        pass

    @abstractmethod
    async def delete_one(self, collection: str, data: dict, *args, **kwargs):
        pass

    @abstractmethod
    async def find(self, collection: str, query: dict, *args, **kwargs):
        pass

    @abstractmethod
    async def drop_collections(self):
        pass

    @abstractmethod
    async def count(self, collection: str, query: dict, *args, **kwargs) -> int:
        pass


class AsyncMongoDB(AsyncDBStorage):
    db: AsyncIOMotorDatabase = None

    def __init__(self):
        self.cl: AsyncIOMotorClient | None = None

    def init_db(self, db_name):
        self.db = self.cl[db_name]
        pass

    async def exec_command(self, db_name: str, command: dict, *args, **kwargs):
        res = await self.cl[db_name].command(command)
        return res

    async def insert_one(self, collection: str, data: dict,  *args, **kwargs):
        return await self.db.get_collection(collection).insert_one(data)

    async def update_one(self, collection: str, data: dict, *args, **kwargs):
        pass

    async def delete_one(self, collection: str, data: dict, *args, **kwargs):
        pass

    async def find(self, collection: str, query: dict, *args, **kwargs):
        pass

    async def count(self, collection: str, query: dict, *args, **kwargs) -> int:
        return await self.db.get_collection(collection).count_documents(query)

    async def drop_collections(self):
        for collection in self.db.list_collection_names():
            self.db.drop_collection(collection)


mdb = AsyncMongoDB()


async def get_mongodb() -> AsyncMongoDB:
    """ Get elasticsearch object. """

    return mdb
