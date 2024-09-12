from http import HTTPStatus


def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"ping": "pong!"}
