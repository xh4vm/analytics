""" Base class for models. """

from datetime import datetime

import orjson
from bson import ObjectId
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    """ Get from json."""

    return orjson.dumps(v, default=default).decode()


class BaseMixin(BaseModel):
    """ Class parent for models. """

    class Config:

        json_loads = orjson.loads
        json_dumps = orjson_dumps
        cache_free = False


class DateMixin(BaseModel):
    created: datetime = None
    modified: datetime = None


class ResponseMDB(BaseModel):
    result: bool


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

    # def __str__(self):
    #     print(str(self))
    #     return str(self)
    #
    # def __repr__(self):
    #     print('repr')
    #     return self.__str__()


async def get_obj(model, string_value: str | None):
    """ Get object from str.

    Arguments:
        model: model of object which need get
        string_value: string value for convert
    """
    if string_value is None:
        return None

    raw_json = orjson.loads(string_value)

    if isinstance(raw_json, list):
        value = [model.parse_raw(raw, encoding='utf-8') for raw in raw_json]
    else:
        value = model(**raw_json)

    return value


async def get_str(obj) -> str:
    """ Get string from object.

    Arguments:
        obj: object for convert to string.

    Returns:
        str: result
    """

    if isinstance(obj, list):
        value = orjson.dumps([row.json() for row in obj])
    else:
        value = obj.json()
    return value


class CountDocs(BaseMixin):
    """ Class for count information."""

    count: int
