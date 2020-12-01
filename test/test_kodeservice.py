from typing import Any

import pytest

from kodealpha import KodeAppFactory
from kodealpha.strings import GENERAL_RESPONSES


@pytest.fixture
async def client(aiohttp_client: Any):
    # Note: aiohttp_client requires pytest-aiohttp installed.
    app = KodeAppFactory().create_app()
    return await aiohttp_client(app)


async def test_root_handling(client) -> None:
    response = await client.get('/')
    assert response.status == 200


async def test_general_handler_with_no_message(client) -> None:
    response = await client.get('/api/general')
    assert response.status == 200

    content = await response.content.read()
    assert GENERAL_RESPONSES['GENERAL_REPLY'] in content.decode()


async def test_general_handler_with_greeting(client) -> None:
    response = await client.get('/api/general/hello there')
    assert response.status == 200

    content = await response.content.read()
    assert GENERAL_RESPONSES['REPLY_TO_GREETING'] in content.decode()


async def test_general_handler_with_insulting(client) -> None:
    response = await client.get('/api/general/you moron')
    assert response.status == 200

    content = await response.content.read()
    assert GENERAL_RESPONSES['REPLY_TO_INSULTING'] in content.decode()
