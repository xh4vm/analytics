from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_get_reviews_list_positive(make_request):
    response = await make_request("get", "/reviews")

    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_reviews_list_negative(make_request):
    response = await make_request("get", "/reviews", invalid_token=True)

    assert response.status == HTTPStatus.FORBIDDEN
