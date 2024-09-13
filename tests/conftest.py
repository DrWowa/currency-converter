import pytest
from fastapi.testclient import TestClient

from app import cache, config, main


@pytest.fixture()
def client():
    return TestClient(main.app)


@pytest.fixture()
def auth_headers():
    return {"X-API-KEY": config.settings.api_key}


@pytest.fixture()
async def redis_rates():
    async with cache.with_cache() as client:
        await cache.set_rates(client, "USD", {"JPY": 1 / 150}, {"success": "true"})
        await cache.set_rates(client, "EUR", {"JPY": 0.05}, {"success": "true"})
        await cache.set_rates(client, "JPY", {"EUR": 1 / 0.05, "USD": 150}, {"success": "true"})


@pytest.fixture(autouse=True)
async def patch_get(monkeypatch):
    from httpx import AsyncClient

    async def _mock(*_, **__):
        return None

    monkeypatch.setattr(AsyncClient, "get", _mock)
