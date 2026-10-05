import requests

BASE_URL = "http://127.0.0.1:5000"
TIMEOUT = 10

def _get(path):
    """GET a path and return parsed JSON, or None on error."""
    try:
        r = requests.get(f"{BASE_URL}{path}", timeout=TIMEOUT)
    except requests.RequestException as e:
        print(f"  [error] {e}")
        return None
    if r.status_code >= 400:
        print(f"  [error] HTTP {r.status_code}: {r.text}")
        return None
    return r.json()


def _post(path, body=None):
    """POST to a path and return parsed JSON or None on error."""
    try:
        r = requests.post(f"{BASE_URL}{path}", json=body, timeout=TIMEOUT)
    except requests.RequestException as e:
        print(f"  [error] {e}")
        return None
    if r.status_code >= 400:
        print(f"  [error] HTTP {r.status_code}: {r.text}")
        return None
    return r.json() if r.text else {}


def _patch(path, body):
    """PATCH a path and return parsed JSON or None on error."""
    try:
        r = requests.patch(f"{BASE_URL}{path}", json=body, timeout=TIMEOUT)
    except requests.RequestException as e:
        print(f"  [error] {e}")
        return None
    if r.status_code >= 400:
        print(f"  [error] HTTP {r.status_code}: {r.text}")
        return None
    return r.json()


def _delete(path):
    """DELETE a path. Returns True on success, False on error."""
    try:
        r = requests.delete(f"{BASE_URL}{path}", timeout=TIMEOUT)
    except requests.RequestException as e:
        print(f"  [error] {e}")
        return False
    if r.status_code >= 400:
        print(f"  [error] HTTP {r.status_code}: {r.text}")
        return False
    return True


def _pretty(item):
    """Print a single inventory item in a readable way."""
    p = item.get("product", {})
    print(f"  ID:         {item.get('id')}")
    print(f"  Name:       {p.get('product_name', '?')}")
    print(f"  Brand:      {p.get('brands', '?')}")
    print(f"  Barcode:    {p.get('barcode', '?')}")
    print(f"  Price:      {item.get('price')}")
    print(f"  Stock:      {item.get('stock')}")
    print(f"  Status:     {item.get('status')}")
    print()



def list_inventory():
    print("\n--- All Inventory ---")
    items = _get("/inventory")
    if not items:
        print("  (empty)")
        return
    for item in items:
        _pretty(item)


def view_item():
    try:
        item_id = int(input("  Enter item ID: "))
    except ValueError:
        print("  [error] ID must be a number")
        return

    print()
    item = _get(f"/inventory/{item_id}")
    if item:
        _pretty(item)


def add_item():
    print("\n--- Add New Item ---")
    name = input("  Product name: ").strip()
    brands = input("  Brand: ").strip()
    barcode = input("  Barcode (optional): ").strip()
    try:
        price = float(input("  Price: ") or 0)
        stock = int(input("  Stock: ") or 0)
    except ValueError:
        print("  [error] Price must be a number, stock must be an integer")
        return

    body = {
        "product_name": name,
        "brands": brands,
        "barcode": barcode,
        "price": price,
        "stock": stock,
    }

    result = _post("/inventory", body)
    if result:
        print("\n  ✔ Created:")
        _pretty(result)


def update_item():
    try:
        item_id = int(input("  Enter item ID to update: "))
    except ValueError:
        print("  [error] ID must be a number")
        return

    print("  Leave a field blank to skip it.")
    updates = {}

    name = input("  New product name: ").strip()
    if name:
        updates["product"] = {"product_name": name}

    brands = input("  New brand: ").strip()
    if brands:
        updates.setdefault("product", {})["brands"] = brands

    price = input("  New price: ").strip()
    if price:
        try:
            updates["price"] = float(price)
        except ValueError:
            print("  [error] Price must be a number")
            return

    stock = input("  New stock: ").strip()
    if stock:
        try:
            updates["stock"] = int(stock)
        except ValueError:
            print("  [error] Stock must be an integer")
            return

    if not updates:
        print("  Nothing to update.")
        return

    result = _patch(f"/inventory/{item_id}", updates)
    if result:
        print("\n  ✔ Updated:")
        _pretty(result)


def delete_item():
    try:
        item_id = int(input("  Enter item ID to delete: "))
    except ValueError:
        print("  [error] ID must be a number")
        return

    confirm = input(f"  Delete item {item_id}? (y/N): ").strip().lower()
    if confirm != "y":
        print("  Cancelled.")
        return

    if _delete(f"/inventory/{item_id}"):
        print(f"  ✔ Deleted item {item_id}.")
    else:
        print("  Delete failed.")


def import_from_external():
    print("\n--- Import from OpenFoodFacts ---")
    barcode = input("  Enter barcode: ").strip()
    if not barcode:
        print("  Cancelled.")
        return

    result = _post(f"/external/import/{barcode}")
    if result:
        print("\n  ✔ Imported and saved:")
        _pretty(result)


# ---------- Main loop ----------
MENU = """Inventory Management System
---------------------------
1. List all inventory
2. View an item
3. Add a new item
4. Update an item
5. Delete an item
6. Import from OpenFoodFacts0. Exit
"""
 
def main():
    while True:
        print(MENU)
        choice = input("  Choose an option: ").strip()

        if choice == "1":
            list_inventory()
        elif choice == "2":
            view_item()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            import_from_external()
        elif choice == "0":
            print("  Goodbye.")
            break
        else:
            print("  [error] Invalid choice.")

        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()