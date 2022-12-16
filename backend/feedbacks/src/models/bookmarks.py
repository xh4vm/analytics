from bson import ObjectId
from pydantic import Field, validator

from .base import BaseMixin, DateMixin, PyObjectId


class Bookmark(BaseMixin, DateMixin):
    """ Class for user's bookmarks model. """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    film_id: str

    class Config:
        collection = 'bookmarks'
        alias = 'Bookmarks'
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @validator('id')
    def replace_none_to_list(cls, v):
        return str(v)
