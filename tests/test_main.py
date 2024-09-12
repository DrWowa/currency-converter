from http import HTTPStatus

import pytest

from app.main import convert


def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"ping": "pong!"}


_convert_options = (
    # "from_symbol", "to_symbol", "amount", "rates", "expected"
    ("USD", "JPY", 2, {"JPY": {"USD": 150}}, 300),
    ("JPY", "EUR", 1_000, {"EUR": {"JPY": 0.05}}, 50),
    # inversed rate
    ("USD", "JPY", 2, {"USD": {"JPY": 1 / 150}}, 300),
    ("JPY", "EUR", 1_000, {"JPY": {"EUR": 1 / 0.05}}, 50),
    # no rate
    ("USD", "JPY", 2, {"USD": None}, None),
    ("USD", "JPY", 2, {}, None),
)


@pytest.mark.parametrize(
    ("from_symbol", "to_symbol", "amount", "rates", "expected"),
    _convert_options,
)
def test_convert(from_symbol, to_symbol, amount, rates, expected):
    assert convert(from_symbol, to_symbol, amount, rates) == expected
