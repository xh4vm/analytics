""" Router for Reviews service. """

from api.v1.params import (CustomQueryParams, CustomReviewsLikesParams,
                           CustomReviewsParams, FilmUserIDsParams,
                           RatingParams, ReviewUserIDsParams)
from api.v1.utilitys import check_result
from fastapi import APIRouter, Body, Depends, Request
from models.base import ResponseMDB
from models.review import ReviewFull, ReviewLike
from services.review import Review, ReviewService, get_review_service

router = APIRouter()


@router.get(
    '',
    response_model=list[ReviewFull],
    summary='Get list of films reviews.',
    description='Get list of films reviews.',
    response_description='Get list of films reviews.',
    tags=['Reviews'],
)
async def get_reviews_list(
        request: Request,
        params: CustomQueryParams = Depends(),
        filters: CustomReviewsParams = Depends(),
        filters_likes: CustomReviewsLikesParams = Depends(),
        obj_service: ReviewService = Depends(get_review_service),
) -> [ReviewFull]:
    """ Create a film review.

    Arguments:
        request: request
        params:
        filters:
        filters_likes:
        obj_service: service object

    Returns:
        Like: user's like of films
    """
    reviews = await obj_service.get_reviews_list(
        params=params,
        filters=filters.get_dict(),
        filters_likes=filters_likes.get_dict(),
    )
    await check_result(reviews, obj_service.errors, obj_service.messages.list_empty)

    return reviews


@router.post(
    '/review',
    response_model=Review,
    summary='Create a film review.',
    description='Create a film review.',
    response_description='Create a film review.',
    tags=['Reviews'],
)
async def create_review(
        request: Request,
        params: FilmUserIDsParams = Depends(),
        text_review: str = Body(description='Text of film review', default='Text of film review.'),
        obj_service: ReviewService = Depends(get_review_service),
) -> Review:
    """ Create a film review.

    Arguments:
        request: request
        params:
        text_review:
        obj_service: service object

    Returns:
        Like: user's like of films
    """
    review = await obj_service.create_doc({**params.get_dict(), 'text': text_review})
    await check_result(review, obj_service.errors, obj_service.messages.list_empty)

    return review


@router.put(
    '/review',
    response_model=Review,
    summary='Update a film review.',
    description='Update a film review.',
    response_description='Update a film review.',
    tags=['Reviews'],
)
async def update_review(
        request: Request,
        params: FilmUserIDsParams = Depends(),
        text_review: str = Body(description='Text of film review', default='Text of film review.'),
        obj_service: ReviewService = Depends(get_review_service),
) -> Review:
    """ Update a film review.

    Arguments:
        request: request
        params:
        text_review:
        obj_service: service object

    Returns:
        Like: user's like of films
    """
    review = await obj_service.update_review({**params.get_dict(), 'text': text_review})
    await check_result(review, obj_service.errors, obj_service.messages.list_empty)

    return review


@router.delete(
    '/review',
    response_model=ResponseMDB,
    summary='Delete a film review.',
    description='Delete a film review.',
    response_description='Delete a film review.',
    tags=['Reviews'],
)
async def delete_review(
        request: Request,
        params: FilmUserIDsParams = Depends(),
        obj_service: ReviewService = Depends(get_review_service),
) -> ResponseMDB:
    """ Delete a film review.

    Arguments:
        request: request
        params:
        obj_service: service object

    Returns:
        Like: user's like of films
    """
    result = await obj_service.delete_doc(params.get_dict())
    await check_result(result, obj_service.errors, obj_service.messages.list_empty)

    return result


@router.post(
    '/review/like',
    response_model=ReviewLike,
    summary='Create a review like.',
    description='Create a review like.',
    response_description='Create a review like.',
    tags=['Reviews'],
)
async def create_review_like(
        request: Request,
        params: ReviewUserIDsParams = Depends(),
        rating: RatingParams = Depends(),
        obj_service: ReviewService = Depends(get_review_service),
) -> Review:
    """ Create like or dislike of review.

    Arguments:
        request: request
        params:
        rating:
        obj_service: service object

    Returns:
        Like: user's like of films
    """
    review = await obj_service.create_review_like({**params.get_dict(), 'rating': rating.rating}, model=ReviewLike)
    await check_result(review, obj_service.errors, obj_service.messages.list_empty)

    return review
