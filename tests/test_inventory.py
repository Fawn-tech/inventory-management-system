import pytest
import inventory


@pytest.fixture(autouse=True)
def reset_inventory():
    """
    Reset inventory_db to a known state before each test.
    Prevents tests from polluting each other.
    """
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
            "price": 4.99,
            "stock": 25
        },
        {
            "id": 2,
            "status": "1",
            "product": {
                "product_name": "Test Bread",
                "brands": "TestBrand",
                "ingredients_text": "flour, water",
                "barcode": "2222222222222"
            },
            "price": 3.49,
            "stock": 12
        }
    ]
    inventory.inventory_db.clear()
    inventory.inventory_db.extend(original)
    inventory._next_id = 3
    yield
    # cleanup happens automatically on next fixture call


# ---------- get_all ----------

def test_get_all_returns_list():
    items = inventory.get_all()
    assert isinstance(items, list)
    assert len(items) == 2


# ---------- get_one ----------

def test_get_one_found():
    item = inventory.get_one(1)
    assert item is not None
    assert item["id"] == 1
    assert item["product"]["product_name"] == "Test Milk"


def test_get_one_not_found():
    assert inventory.get_one(999) is None


# ---------- create ----------

def test_create_assigns_id_and_appends():
    new = inventory.create({
        "product": {"product_name": "New Item", "brands": "X"},
        "price": 1.5,
        "stock": 10
    })
    assert new["id"] == 3
    assert new["product"]["product_name"] == "New Item"
    assert new["price"] == 1.5
    assert new["stock"] == 10
    assert len(inventory.get_all()) == 3


def test_create_uses_defaults_when_fields_missing():
    new = inventory.create({"product": {"product_name": "Sparse"}})
    assert new["price"] == 0.0
    assert new["stock"] == 0


def test_create_increments_counter():
    inventory.create({"product": {"product_name": "A"}})
    second = inventory.create({"product": {"product_name": "B"}})
    assert second["id"] == 4


# ---------- update ----------

def test_update_changes_field():
    updated = inventory.update(1, {"price": 99.0})
    assert updated["price"] == 99.0
    assert inventory.get_one(1)["price"] == 99.0


def test_update_nested_product_field():
    updated = inventory.update(1, {"product": {"brands": "NewBrand"}})
    assert updated["product"]["brands"] == "NewBrand"


def test_update_missing_item_returns_none():
    assert inventory.update(999, {"price": 1.0}) is None


def test_update_ignores_id_change():
    inventory.update(1, {"id": 999})
    assert inventory.get_one(1) is not None
    assert inventory.get_one(999) is None



def test_delete_existing_returns_true():
    assert inventory.delete(1) is True
    assert inventory.get_one(1) is None
    assert len(inventory.get_all()) == 1


def test_delete_missing_returns_false():
    assert inventory.delete(999) is False
    assert len(inventory.get_all()) == 2