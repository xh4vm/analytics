""" Base class for models. """

import orjson
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


class ResponseMDB(BaseModel):
    result: bool


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
