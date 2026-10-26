from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_explains_known_movement():
    response = client.post(
        "/v1/explanations",
        json={
            "movement": {
                "code": "123",
                "description": "Conclusos para decisão",
                "date": "2026-10-26",
            },
            "language": "pt-BR",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert "encaminhado" in body["data"]["explanation"]
    assert body["data"]["limitations"]


def test_unknown_movement_returns_limitation():
    response = client.post(
        "/v1/explanations",
        json={
            "movement": {
                "code": "999",
                "description": "Movimentação ainda não cadastrada",
            },
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert "não consigo explicar" in body["data"]["explanation"]
    assert body["data"]["limitations"]


def test_empty_description_is_rejected():
    response = client.post(
        "/v1/explanations",
        json={
            "movement": {
                "code": "123",
                "description": "   ",
            },
        },
    )

    assert response.status_code == 422


def test_invalid_date_is_rejected():
    response = client.post(
        "/v1/explanations",
        json={
            "movement": {
                "code": "123",
                "description": "Conclusos para decisão",
                "date": "data-invalida",
            },
        },
    )

    assert response.status_code == 422