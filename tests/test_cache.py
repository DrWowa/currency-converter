from app import cache


async def test_connection():
    client = await cache.get_client()
    assert await client.ping()


async def test_context():
    async with cache.with_cache() as client:
        assert await client.ping()
