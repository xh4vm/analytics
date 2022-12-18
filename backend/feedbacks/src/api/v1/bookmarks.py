""" Router for Films service. """

from src.api.v1.params import FilmUserIDsParams
from src.api.v1.utilitys import check_result
from fastapi import APIRouter, Depends, Request
from src.models.base import ResponseMDB
from src.models.bookmarks import Bookmark
from pydantic.types import UUID4
from src.services.bookmark import BookmarkService, get_bookmark_service
from modules.auth.src.payloads.fastapi import UserAccessRequired

router = APIRouter()
URL = f'{CONFIG.FEEDBACKS_API_HOST}:{CONFIG.FEEDBACKS_API_PORT}{CONFIG.FEEDBACKS_API_PATH}/{CONFIG.FEEDBACKS_API_VERSION}/bookmarks'


@router.get(
    '{film_id}',
    response_model=list[Bookmark],
    summary='Get list of user\'s bookmarks.',
    description='Get list of user\'s bookmarks.',
    response_description='Get list of user\'s bookmarks.',
    tags=['Bookmarks'],
)
async def get_list_user_bookmarks(
        request: Request,
        user_id: UUID4,
        current_user_id: str = Depends(UserAccessRequired(permissions={URL: 'GET'})),
        obj_service: BookmarkService = Depends(get_bookmark_service),
) -> [Bookmark]:
    """ Get list of user\'s bookmarks.

    Arguments:
        request: request
        user_id:
        obj_service: service object

    Returns:
        list[Bookmark]: list of user\'s bookmarks.
    """
    bookmarks = await obj_service.get_doc_list(user_id=str(user_id))
    await check_result(bookmarks, obj_service.errors, obj_service.messages.list_empty)

    return bookmarks


@router.post(
    '/bookmark',
    response_model=Bookmark,
    summary='Create a user\'s bookmark.',
    description='Create a user\'s bookmark.',
    response_description='Create a user\'s bookmark.',
    tags=['Bookmarks'],
)
async def create_bookmark(
        request: Request,
        params: FilmUserIDsParams = Depends(),
        current_user_id: str = Depends(UserAccessRequired(permissions={URL: 'POST'})),
        obj_service: BookmarkService = Depends(get_bookmark_service),
) -> Bookmark:
    """ Create a user\'s bookmark.

    Arguments:
        request: request
        params:
        obj_service: service object

    Returns:
        Bookmark: user\'s bookmark.
    """
    bookmark = await obj_service.create_doc(params.get_dict())
    await check_result(bookmark, obj_service.errors, obj_service.messages.list_empty)

    return bookmark


@router.delete(
    '/bookmark',
    response_model=ResponseMDB,
    summary='Delete a user\'s bookmark.',
    description='Delete a user\'s bookmark.',
    response_description='Delete a user\'s bookmark.',
    tags=['Bookmarks'],
)
async def delete_bookmark(
        request: Request,
        params: FilmUserIDsParams = Depends(),
        current_user_id: str = Depends(UserAccessRequired(permissions={URL+'/bookmark': 'DELETE'})),
        obj_service: BookmarkService = Depends(get_bookmark_service),
) -> ResponseMDB:
    """ Delete a user\'s bookmark..

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
