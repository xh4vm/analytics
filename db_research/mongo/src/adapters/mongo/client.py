from dataclasses import dataclass

from adapters.base import BaseDBClient
from core.settings import mongo_settings
from pymongo import MongoClient
from pymongo.database import Database
from utility.utility import get_time


@dataclass
class MongoBDClient(BaseDBClient):
    client_db: Database = None
    db_name: str = None
    client: MongoClient = None

    def connect(self):
        self.client = MongoClient(self.connection_string)

    def get_database(self):
        self.client_db = self.client[self.db_name]
        self.client.admin.command('enableSharding', self.db_name)

    @get_time
    def exec_command(self, scope: str, command: dict) -> dict:
        db_name, collection_name, comm = scope.split('.')
        return self.client[db_name].command(command)

    def drop_collection(self):
        for collection in self.client_db.list_collection_names():
            self.client_db.drop_collection(collection)

    @get_time
    def insert_one(self, collection: str, data: dict):
        return self.client_db[collection].insert_one(data)

    @get_time
    def insert_many(self, collection: str, data: dict):
        return self.client_db[collection].insert_many(data)


database_client = MongoBDClient(connection_string=mongo_settings.CONNECT_STRING, db_name=mongo_settings.DATABASE)
database_client.connect()
database_client.get_database()
