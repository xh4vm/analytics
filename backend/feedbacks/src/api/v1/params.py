# General classes for routers
from fastapi import Body
from pydantic.types import UUID4


class FilmUserIDsParams:
    """ Class general query parameters."""
    def __init__(
        self,
        film_id: UUID4 = Body(
            description="ID of film",
        ),
        user_id: UUID4 = Body(
            description="ID of user",
        ),
    ):
        self.film_id = film_id
        self.user_id = user_id
