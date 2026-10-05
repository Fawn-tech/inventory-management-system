

# a list of product dictionaries
inventory_db = [
    {
        "id": 1,
        "status": "1",
        "product": {
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar, vitamin D2, vitamin B12",
        "barcode": "0025293001568"
        },
        "price":100.0,
        "stock": 25,
    },
        
    {
        "id": 2,
        "status": "1",
        "product": {
            "product_name": "Whole Wheat Bread",
            "brands": "Nature's Own",
            "ingredients_text": "Whole wheat flour, water, yeast, salt, sugar",
            "barcode": "0072250050047"
        },
        "price":150.0,
        "stock": 12,
        
    },
    {
        "id": 3,
        "status": "1",
        "product": {
            "product_name": "Greek Yogurt",
            "brands": "Chobani",
            "ingredients_text": "Cultured pasteurized nonfat milk, live active cultures",
            "barcode": "0894700010225"
        },
        "price": 180.0,
        "stock": 40,
    },
    {
        "id": 4,
        "status": "1",
        "product": {
            "product_name": "Peanut Butter",
            "brands": "Jif",
            "ingredients_text": "Roasted peanuts, sugar, molasses, fully hydrogenated vegetable oils",
            "barcode": "0051500255170"
        },
        "price": 600.0,
        "stock": 18,
        
    },
    {
        "id": 5,
        "status": "1",
        "product": {
            "product_name": "Sparkling Water",
            "brands": "LaCroix",
            "ingredients_text": "Carbonated water, natural flavors",
            "barcode": "0012322000804"
        },
        "price": 200.0,
        "stock": 60,
        
    }
]

_next_id = 6


def get_all():
    """Return the entire inventory as a list of dicts."""
    return inventory_db


def get_one(item_id):
    """Return a single item by ID or None if not found."""
    for item in inventory_db:
        if item["id"] == item_id:
            return item
    return None


def create(data):
    """Add a new item to the inventory. Auto-assigns an ID."""
    global _next_id

    new_item = {
        "id": _next_id,
        "status": data.get("status", "1"),
        "product": data.get("product", {}),
        "price": float(data.get("price", 0.0)),
        "stock": int(data.get("stock", 0)),
        
    }
    inventory_db.append(new_item)
    _next_id += 1
    return new_item


def update(item_id, data):
    """Partially update an existing item."""
    item = get_one(item_id)
    if item is None:
        return None

    for key, value in data.items():
        if key in item and key != "id":
            item[key] = value

    return item


def delete(item_id):
    """Delete an item by ID. Returns True if deleted, False if not found."""
    for i, item in enumerate(inventory_db):
        if item["id"] == item_id:
            inventory_db.pop(i)
            return True
    return False