import pytest
from starlette.testclient import TestClient

from app import cache, main


@pytest.fixture()
def client():
    return TestClient(main.app)


@pytest.fixture()
async def redis_rates():
    await cache.set_rates("USD", {"JPY": 1 / 150})
    await cache.set_rates("EUR", {"JPY": 0.05})
