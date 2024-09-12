from urllib.parse import urljoin

from httpx import AsyncClient

from app.config import settings


async def get_latest_rates(symbol):
    if not settings.exchangeratesapi.has_access_to_base and symbol != "EUR":
        return None

    params = {"access_key": settings.exchangeratesapi.access_key}
    if settings.exchangeratesapi.has_access_to_base:
        params["base"] = symbol

    client = AsyncClient()
    response = await client.get(
        urljoin(settings.exchangeratesapi.base_url, "latest"),
        params=params,
    )
    data = response.json()
    if data.get("success", None):
        return data

    return None
    # TODO: errors logging
