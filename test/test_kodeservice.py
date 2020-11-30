import pytest
from typing import Any
from kodealpha import KodeAppFactory


@pytest.fixture
async def client(aiohttp_client: Any):
    # Note: aiohttp_client requires pytest-aiohttp installed.
    app = KodeAppFactory().create_app()
    return await aiohttp_client(app)


async def test_root_handling(client) -> None:
    response = await client.get('/')
    assert response.status == 200
