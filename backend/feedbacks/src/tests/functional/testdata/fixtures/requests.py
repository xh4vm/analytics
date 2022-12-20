from dataclasses import dataclass
from typing import Optional

import aiohttp
import pytest
from multidict import CIMultiDictProxy

BASE_URL = "http://{app_host}:{app_port}/api/v1".format(
    app_host="127.0.0.1", app_port="8080"
)


@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Authorization-Token": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwicGVybWlzc2lvbnMiOnsiMjA4MmM1ZjJhOGE4NTMzMjcyNjQ4MmIyMDA4NWQzOWIiOlsiR0VUIiwiUE9TVCIsIlBVVCIsIkRFTEVURSJdLCJlZTBhY2M3MGU4ZGFkOGEyYmE3Zjg5Y2VhMDZiMWFhYiI6WyJHRVQiLCJQT1NUIiwiUFVUIiwiREVMRVRFIl0sIjE1YzkyOGU1ZmNkNzkzNzRjYzVhZTg5Mzg0MjQxZWRjIjpbIkdFVCIsIlBPU1QiLCJQVVQiLCJERUxFVEUiXSwiZGJkMzBkNjUxYTE3MTRkZTg0NzFiMjIyM2MyMTg0NjciOlsiR0VUIiwiUE9TVCIsIlBVVCIsIkRFTEVURSJdLCIxY2M2NzdhNWIwZTg4MmIzNGY1MjRiODg4MmJjYTQ0NiI6WyJHRVQiLCJQT1NUIiwiUFVUIiwiREVMRVRFIl0sIjM5YWVkMWI3NTM1NjhjNzg1NzFjODRkZDNhYmYwM2E5IjpbIkdFVCIsIlBPU1QiLCJQVVQiLCJERUxFVEUiXSwiMzgyYzQyOTY1ODA2NmZjZDA1ZjZlNzVjYjY3Y2Y4ZjkiOlsiR0VUIiwiUE9TVCIsIlBVVCIsIkRFTEVURSJdLCI0ZGNhM2VlN2JhYjI4YmQ5Mzc4N2RiNjE0YjVlNzk5YiI6WyJHRVQiLCJQT1NUIiwiUFVUIiwiREVMRVRFIl0sIjVmMGNiYjZjMjk1NjM5M2I4Njg2OGM2ZjJjY2YyNWQ3IjpbIkdFVCIsIlBPU1QiLCJQVVQiLCJERUxFVEUiXX0sImV4cCI6MjA3MDkyNTA4NCwiaWF0IjoxNjY5OTI1MDg0fQ.PnXq7znGE2-8vijXrzly45hv3ZmVw0Bs9W3E1psKmuc",
        }
    )
    yield session
    await session.close()


@pytest.fixture(scope="session")
async def session_invalid_token():
    session = aiohttp.ClientSession(
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Authorization-Token": "1",
        }
    )
    yield session
    await session.close()


@dataclass
class HTTPResponse:
    body: dict | list
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture
def make_request(session, session_invalid_token):
    async def inner(
        method: str,
        url: str,
        params: Optional[dict] = None,
        invalid_token: bool = False,
    ) -> HTTPResponse:
        params = params or {}
        _session = session if not invalid_token else session_invalid_token
        _method = _session.get
        if method.lower() == 'post':
            _method = _session.post
        async with _method(BASE_URL + url, params=params) as response:
            return HTTPResponse(
                body=await response.json() if response.ok else {},
                headers=response.headers,
                status=response.status,
            )

    return inner
