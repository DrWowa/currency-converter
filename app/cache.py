from contextlib import asynccontextmanager

import redis.asyncio as aioredis

from app.config import settings


async def get_client():
    return aioredis.StrictRedis.from_url(
        url=settings.redis.url,
        max_connections=settings.redis.max_connections,
        decode_responses=True,
    )


@asynccontextmanager
async def with_cache():
    client = await get_client()
    yield client
    await client.aclose()


async def get_rates(from_symbol, to_symbol):
    result = {}
    async with with_cache() as client:
        result[from_symbol] = _decode_rates(await client.hgetall(_rate_key(from_symbol)))
        result[to_symbol] = _decode_rates(await client.hgetall(_rate_key(to_symbol)))

    return result


async def set_rates(symbol, rates):
    async with with_cache() as client:
        await client.hset(_rate_key(symbol), mapping=rates)


def _rate_key(symbol):
    return f"{symbol}-RATE"


def _decode_rates(rates):
    return {key: float(val) for key, val in rates.items()}
