from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import backoff
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


@dataclass
class BaseDBClient(ABC):
    connection_string: str
    client: MongoClient | Any = None

    @abstractmethod
    def connect(self):
        pass

    @backoff.on_exception(
        backoff.expo, (ConnectionRefusedError, ConnectionFailure, ServerSelectionTimeoutError), max_tries=1
    )
    def execute(self, text: str):
        if not self.connection:
            self.connect()
        return self.connection.execute(text)
