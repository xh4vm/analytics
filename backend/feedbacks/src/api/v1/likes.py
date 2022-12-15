""" Router for Films service. """

from api.v1.params import FilmUserIDsParams
from api.v1.utilitys import check_result
from db.redis import use_cache
# from services.film import get_film_service
from fastapi import APIRouter, Body, Depends, Request
from pydantic.types import UUID4
# from fastapi import security
# from fastapi_jwt_auth import AuthJWT
# from pydantic.main import BaseModel
# from pydantic.types import UUID4
#
# from api.v1.params import CustomFilmsParams
# from api.v1.params import CustomQueryParams
# from api.v1.params import FilmSortQueryParam
# from api.v1.utilitys import check_result
# from api.v1.utilitys import prohibit_extra_params
# from core.config import SETTINGS
# from db.redis import use_cache
# from models.base import CountDocs
# from models.film import FilmFull, FilmFullAuthUnavailable
from services.like import FilmsLikes, Like, LikeService, get_like_service

router = APIRouter()


@router.get(
    '/{film_id}',
    response_model=FilmsLikes,
    summary='Number of likes and dislikes of films.',
    description='Number of likes and dislikes of film.',
    response_description='Information about number of likes and dislikes of film',
    tags=['Likes'],
)
@use_cache(model=FilmsLikes)
async def get_films_likes(
        request: Request,
        film_id: UUID4,
        obj_service: LikeService = Depends(get_like_service),
) -> FilmsLikes:
    """ Number of likes and dislikes of films.

    Arguments:
        request: request
        film_id: ID of film
        obj_service: service object

    Returns:
        FilmsLikes: likes of films
    """
    films_likes = await obj_service.get_films_likes(str(film_id))
    await check_result(films_likes, obj_service.errors, obj_service.messages.list_empty)

    return films_likes


@router.post(
    '/like',
    response_model=Like,
    summary='Create likes or dislikes of films.',
    description='Create likes or dislikes of films.',
    response_description='Create likes or dislikes of films.',
    tags=['Likes'],
)
async def create_like(
        request: Request,
        params: FilmUserIDsParams = Depends(),
        rating: int = Body(description="ID of user"),
        obj_service: LikeService = Depends(get_like_service),
) -> Like:
    """ Create likes or dislikes of films.

    Arguments:
        request: request
        params:
        rating:
        obj_service: service object

    Returns:
        Like: user's like of films
    """
    like = await obj_service.create_like(params, rating)
    await check_result(like, obj_service.errors, obj_service.messages.list_empty)

    return like
