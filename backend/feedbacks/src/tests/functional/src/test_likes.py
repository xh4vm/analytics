from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_create_like_positive(make_request):
    response = await make_request(
        "post",
        "/likes/like",
        params={
            "film_id": "53f52d0a-b863-4811-8d63-c625be6e5cd8",
            "user_id": "7f064039-6ffc-48a5-a3b6-597885f1ea6c",
            "rating": 7,
        },
    )

    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_create_like_negative(make_request):
    response = await make_request("post", "/likes/like", invalid_token=True)

    assert response.status == HTTPStatus.FORBIDDEN
