import json
from datetime import datetime
from functools import wraps
from uuid import UUID

import dateutil.parser
from bson import ObjectId
from bson.errors import InvalidId
from bson.timestamp import Timestamp


class DateEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, datetime):
            return obj.isoformat()

        if isinstance(obj, Timestamp):
            return obj.as_datetime().isoformat()

        if isinstance(obj, (ObjectId, bytes)):
            return str(obj)

        return json.JSONEncoder.default(self, obj)


def datetime_parser(json_dict):
    for (key, value) in json_dict.items():

        try:
            json_dict[key] = dateutil.parser.parse(value)
        except (ValueError, AttributeError, TypeError):
            pass

        try:
            json_dict[key] = ObjectId(value)
        except (ValueError, AttributeError, TypeError, InvalidId):
            pass

    return json_dict


def get_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        return result, start_time, datetime.now() - start_time
    return wrapper


def str_if_uuid(value):
    return str(value) if isinstance(value, UUID) else value
