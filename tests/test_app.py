import pytest
from unittest.mock import patch
from app import app
import inventory


@pytest.fixture
def client():
    
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def reset_inventory():
    """Reset inventory to a known state before each test."""
    original = [
        {
            "id": 1,
            "status": "1",
            "product": {
                "product_name": "Test Milk",
                "brands": "TestBrand",
                "ingredients_text": "water, milk",
                "barcode": "1111111111111"
            },
            "price": 500.00,
            "stock": 25
        }
    ]
    inventory.inventory_db.clear()
    inventory.inventory_db.extend(original)
    inventory._next_id = 2
    yield


# ---------- GET /inventory ----------

def test_list_inventory(client):
    r = client.get("/inventory")
    assert r.status_code == 200
    data = r.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["product"]["product_name"] == "Test Milk"


# ---------- GET /inventory/<id> ----------

def test_get_item_found(client):
    r = client.get("/inventory/1")
    assert r.status_code == 200
    assert r.get_json()["id"] == 1


def test_get_item_not_found(client):
    r = client.get("/inventory/999")
    assert r.status_code == 404


# ---------- POST /inventory ----------

def test_create_item(client):
    payload = {
        "product": {"product_name": "New Thing", "brands": "X"},
        "price": 5.5,
        "stock": 3
    }
    r = client.post("/inventory", json=payload)
    assert r.status_code == 201
    data = r.get_json()
    assert data["id"] == 2
    assert data["product"]["product_name"] == "New Thing"


def test_create_item_without_body(client):
    r = client.post("/inventory", json={})
    assert r.status_code == 400


def test_create_item_with_no_json(client):
    r = client.post("/inventory")
    assert r.status_code == 400


# ---------- PATCH /inventory/<id> ----------

def test_update_item(client):
    r = client.patch("/inventory/1", json={"price": 42.0})
    assert r.status_code == 200
    assert r.get_json()["price"] == 42.0


def test_update_item_not_found(client):
    r = client.patch("/inventory/999", json={"price": 1.0})
    assert r.status_code == 404


def test_update_item_without_body(client):
    r = client.patch("/inventory/1", json={})
    assert r.status_code == 400


# ---------- DELETE /inventory/<id> ----------

def test_delete_item(client):
    r = client.delete("/inventory/1")
    assert r.status_code == 204
    assert inventory.get_one(1) is None


def test_delete_item_not_found(client):
    r = client.delete("/inventory/999")
    assert r.status_code == 404


# ---------- External API (mocked) ----------

MOCK_PRODUCT = {
    "product": {
        "product_name": "Mocked Nutella",
        "brands": "Ferrero",
        "ingredients_text": "sugar, palm oil, hazelnuts",
        "barcode": "3017620422003"
    }
}


@patch("external_api.fetch_by_barcode", return_value=MOCK_PRODUCT)
def test_external_fetch_only(mock_fetch, client):
    r = client.get("/external/product/3017620422003")
    assert r.status_code == 200
    assert r.get_json()["product"]["product_name"] == "Mocked Nutella"
    mock_fetch.assert_called_once_with("3017620422003")


@patch("external_api.fetch_by_barcode", return_value=None)
def test_external_fetch_not_found(mock_fetch, client):
    r = client.get("/external/product/0000000000000")
    assert r.status_code == 404


@patch("external_api.fetch_by_barcode", return_value=MOCK_PRODUCT)
def test_external_import_adds_to_inventory(mock_fetch, client):
    r = client.post("/external/import/3017620422003")
    assert r.status_code == 201
    data = r.get_json()
    assert data["id"] == 2
    assert data["product"]["product_name"] == "Mocked Nutella"
    assert len(inventory.get_all()) == 2


@patch("external_api.fetch_by_barcode", return_value=None)
def test_external_import_not_found(mock_fetch, client):
    r = client.post("/external/import/0000000000000")
    assert r.status_code == 404