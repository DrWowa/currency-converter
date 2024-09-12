from contextlib import asynccontextmanager

import redis.asyncio as aioredis

from app.config import settings
from app.exchangeratesapi import get_latest_rates


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
        for symbol in (from_symbol, to_symbol):
            rates = await client.hgetall(_rate_key(symbol))
            if not rates:
                rates = await _process_new_rates(client, symbol)

            flag = await client.get(_timer_key(symbol))
            if not flag and rates:
                rates = await _process_new_rates(client, symbol)

            result[symbol] = _decode_rates(rates)

    return result


async def set_rates(client, symbol, rates, data):
    await client.hset(_data_key(symbol), mapping=data)
    await client.hset(_rate_key(symbol), mapping=rates)
    await client.set(_timer_key(symbol), "set", ex=settings.exchangeratesapi.expire)


def _rate_key(symbol):
    return f"RATES-{symbol}"


def _timer_key(symbol):
    return f"TIMER-{symbol}"


def _data_key(symbol):
    return f"DATA-{symbol}"


def _decode_rates(rates):
    if not rates:
        return None

    return {key: float(val) for key, val in rates.items()}


async def _process_new_rates(client, symbol):
    data = await get_latest_rates(symbol)
    if not data:
        return None

    rates = data.pop("rates")
    data.pop("success")
    await set_rates(client, symbol, rates, data)
    return rates
