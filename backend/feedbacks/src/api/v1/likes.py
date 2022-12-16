""" Router for Likes service. """

from api.v1.params import FilmUserIDsParams, RatingParams
from api.v1.utilitys import check_result
from db.redis import use_cache
from fastapi import APIRouter, Depends, Request
from models.base import ResponseMDB
from models.like import FilmsLikes
from pydantic.types import UUID4
from services.like import FilmsAvgRating, Like, LikeService, get_like_service

router = APIRouter()


@router.get(
    '/count/{film_id}',
    response_model=FilmsLikes,
    summary='Number of likes and dislikes of films.',
    description='Number of likes and dislikes of film.',
    response_description='Information about number of likes and dislikes of film',
    tags=['Likes'],
)
@use_cache(model=FilmsLikes)
async def get_number_films_likes(
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
    films_likes = await obj_service.get_number_doc_likes('film_id', str(film_id), model=FilmsLikes)
    await check_result(films_likes, obj_service.errors, obj_service.messages.list_empty)

    return films_likes


@router.get(
    '/avg/{film_id}',
    response_model=FilmsAvgRating,
    summary='Average of rating of films.',
    description='Average of rating of films.',
    response_description='Average of rating of films.',
    tags=['Likes'],
)
@use_cache(model=FilmsAvgRating)
async def get_films_avg_rating(
        request: Request,
        film_id: UUID4,
        obj_service: LikeService = Depends(get_like_service),
) -> FilmsAvgRating:
    """ Average of rating of films.

    Arguments:
        request: request
        film_id: ID of film
        obj_service: service object

    Returns:
        FilmsAvgRating: average of rating of films
    """
    films_avg_rating = await obj_service.get_film_avg_rating(str(film_id))
    await check_result(films_avg_rating, obj_service.errors, obj_service.messages.list_empty)

    return films_avg_rating


@router.post(
    '/like',
    response_model=Like,
    summary='Create like or dislike of films.',
    description='Create like or dislike of films.',
    response_description='Create like or dislike of films.',
    tags=['Likes'],
)
async def create_like(
        request: Request,
        params: FilmUserIDsParams = Depends(),
        rating: RatingParams = Depends(),
        obj_service: LikeService = Depends(get_like_service),
) -> Like:
    """ Create like or dislike of films.

    Arguments:
        request: request
        params:
        rating:
        obj_service: service object

    Returns:
        Like: user's like of films
    """
    like = await obj_service.create_doc({**params.get_dict(), 'rating': rating.rating})
    await check_result(like, obj_service.errors, obj_service.messages.list_empty)

    return like


@router.put(
    '/like',
    response_model=Like,
    summary='Update user\'s like of films.',
    description='Update user\'s like of films.',
    response_description='Update user\'s like of films.',
    tags=['Likes'],
)
async def update_like(
        request: Request,
        params: FilmUserIDsParams = Depends(),
        rating: RatingParams = Depends(),
        obj_service: LikeService = Depends(get_like_service),
) -> Like:
    """ 'Update user\'s like of films.'.

    Arguments:
        request: request
        params:
        rating:
        obj_service: service object

    Returns:
        Like: user's like of films
    """
    like = await obj_service.update_like({**params.get_dict(), 'rating': rating.rating})
    await check_result(like, obj_service.errors, obj_service.messages.list_empty)

    return like


@router.delete(
    '/like',
    response_model=ResponseMDB,
    summary='Delete user\'s like of films.',
    description='Delete user\'s like of films.',
    response_description='Delete user\'s like of films.',
    tags=['Likes'],
)
async def delete_like(
        request: Request,
        params: FilmUserIDsParams = Depends(),
        obj_service: LikeService = Depends(get_like_service),
) -> ResponseMDB:
    """ 'Delete user\'s like of films.'.

    Arguments:
        request: request
        params:
        obj_service: service object

    Returns:
        ResponseMDB: respond
    """
    result = await obj_service.delete_doc(params.get_dict())
    await check_result(result, obj_service.errors, obj_service.messages.list_empty)

    return result
