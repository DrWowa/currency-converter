from contextlib import asynccontextmanager

import redis.asyncio as aioredis

from app.config import settings


async def get_client():
    return aioredis.StrictRedis.from_url(
        url=settings.redis.url,
        max_connections=settings.redis.max_connections,
    )


@asynccontextmanager
async def with_cache():
    client = await get_client()
    yield client
    await client.aclose()
