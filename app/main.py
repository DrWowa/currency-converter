from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

from app import cache, config

app = FastAPI()

header_api_key = APIKeyHeader(name="x-api-key", auto_error=True)


class ConvertResult(BaseModel):
    from_symbol: str = Field(..., alias="from")
    to_symbol: str = Field(..., alias="to")
    amount: float
    converted_amount: float


def check_api_key(key: str = Depends(header_api_key)):
    if key == config.settings.api_key:
        return key

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API key",
    )


@app.get("/")
async def convert_route(
    from_symbol: Annotated[str, Query(alias="from", min_length=3, max_length=3)],
    to_symbol: Annotated[str, Query(alias="to", min_length=3, max_length=3)],
    amount: Annotated[float, Query(gt=0)],
    _: str = Depends(check_api_key),
) -> ConvertResult:
    from_symbol = from_symbol.upper()
    to_symbol = to_symbol.upper()

    rates = await cache.get_rates(from_symbol, to_symbol)
    result = convert(from_symbol, to_symbol, amount, rates)
    if result is None:
        symbols = [key for key in (from_symbol, to_symbol) if not rates[key]]
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unsupported symbols: {symbols}",
        )

    return {"from": from_symbol, "to": to_symbol, "amount": amount, "converted_amount": result}


def convert(from_symbol, to_symbol, amount, rates):
    rate = (rates.get(to_symbol) or {}).get(from_symbol, None)

    if rate is None:
        rate = (rates.get(from_symbol) or {}).get(to_symbol, None)
        rate = 1 / rate if rate else None

    if rate is None:
        return None

    return amount * rate
