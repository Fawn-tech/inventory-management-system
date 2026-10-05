import requests

BASE_URL = "https://world.openfoodfacts.org/api/v0/product"

# Timeout (seconds) so we don't hang forever if the API is slow
TIMEOUT = 10

HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0 (student project)"
}



def fetch_by_barcode(barcode):

    url = f"{BASE_URL}/{barcode}.json"

    #  Network request
    try:
        response = requests.get(url, timeout=TIMEOUT, headers=HEADERS)
    except requests.RequestException:
        return None

    #  HTTP status
    if response.status_code != 200:
        return None

    #  Parse JSON
    try:
        data = response.json()
    except ValueError:
        return None

    # OpenFoodFacts-specific status flag
    if data.get("status") != 1:
        return None

    # Extract & normalise
    product = data.get("product", {})
    return {
        "product": {
            "product_name": product.get("product_name", "Unknown"),
            "brands": product.get("brands", ""),
            "ingredients_text": product.get("ingredients_text", ""),
            "barcode": barcode,
        }
    }

