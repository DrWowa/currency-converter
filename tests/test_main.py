from urllib.parse import urlencode

import pytest
from fastapi import status

from app.main import convert


@pytest.mark.parametrize(
    ("from_symbol", "to_symbol", "amount", "rates", "expected"),
    (
        ("USD", "JPY", 2, {"JPY": {"USD": 150}}, 300),
        ("JPY", "EUR", 1_000, {"EUR": {"JPY": 0.05}}, 50),
        # inversed rate
        ("USD", "JPY", 2, {"USD": {"JPY": 1 / 150}}, 300),
        ("JPY", "EUR", 1_000, {"JPY": {"EUR": 1 / 0.05}}, 50),
        # no rate
        ("USD", "JPY", 2, {"USD": None}, None),
        ("USD", "JPY", 2, {}, None),
    ),
)
def test_convert(from_symbol, to_symbol, amount, rates, expected):
    assert convert(from_symbol, to_symbol, amount, rates) == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    (
        ({"from": "USD", "to": "JPY", "amount": 2}, 300),
        ({"from": "JPY", "to": "EUR", "amount": 1_000}, 50),
    ),
)
@pytest.mark.usefixtures("redis_rates")
async def test_convert_route(client, auth_headers, data, expected):
    response = client.get("?".join(("/", urlencode(data))), headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data["converted_amount"] = expected
    assert response.json() == data


@pytest.mark.parametrize(
    "data",
    (
        {},
        {"to": "usd", "amount": 10},  # no from
        {"from": "usd", "amount": 10},  # no to
        {"from": "eur", "to": "usd"},  # no amount
    ),
)
async def test_convert_route_fail_on_absent_input(client, auth_headers, data):
    response = client.get(("?".join(("/", urlencode(data)))).strip("?"), headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    ("data", "expected"),
    (
        ({"from": "AAA", "to": "usd", "amount": 10}, "'AAA'"),  # unsupported from
        ({"from": "usd", "to": "BBB", "amount": 10}, "'BBB'"),  # unsupported to
        ({"from": "AAA", "to": "BBB", "amount": 10}, "'AAA', 'BBB'"),  # unsupported both
    ),
)
@pytest.mark.usefixtures("redis_rates")
async def test_convert_route_fail_on_unsupported_symbols(client, auth_headers, data, expected):
    response = client.get(("?".join(("/", urlencode(data)))).strip("?"), headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"detail": f"Unsupported symbols: [{expected}]"}
