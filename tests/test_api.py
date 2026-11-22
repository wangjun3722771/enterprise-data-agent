
from fastapi.testclient import TestClient

from enterprise_data_agent.api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_product():
    response = client.get("/products/1001")

    assert response.status_code == 200
    assert response.json()["name"] == "机械键盘"


def test_product_not_found():
    response = client.get("/products/9999")

    assert response.status_code == 404


def test_invalid_product_id():
    response = client.get("/products/abc")

    assert response.status_code == 422


def test_calculate_order():
    response = client.post(
        "/orders/calculate",
        json={
            "product_name": "机械键盘",
            "price": 299,
            "quantity": 2,
        },
    )

    assert response.status_code == 200
    assert response.json()["total"] == 598.0


def test_invalid_price():
    response = client.post(
        "/orders/calculate",
        json={
            "product_name": "机械键盘",
            "price": -100,
            "quantity": 2,
        },
    )

    assert response.status_code == 422


def test_missing_quantity():
    response = client.post(
        "/orders/calculate",
        json={
            "product_name": "机械键盘",
            "price": 299,
        },
    )

    assert response.status_code == 422

def test_calculate_discount():
    response = client.post(
        "/orders/discount",
        json={
            "price": 299,
            "quantity": 2,
            "discount": 0.1,
        },
    )

    assert response.status_code == 200
    assert response.json()["original_total"] == 598.0
