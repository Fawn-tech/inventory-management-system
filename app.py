from flask import Flask, jsonify, request
import inventory
import external_api

app = Flask(__name__)

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory.get_all()),200

@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = inventory.get_one(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item),200

@app.route('/inventory', methods=['POST'])
def create_item():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    item = inventory.create(data)
    return jsonify(item), 201

@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    item = inventory.update(item_id, data)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item),200

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if not inventory.delete(item_id):
        return jsonify({"error": "Item not found"}), 404
    return "", 204  

@app.route('/external/product/<barcode>', methods=['GET'])
def external_get_product(barcode):
    """Fetch product details from OpenFoodFacts (does not save)."""
    product = external_api.fetch_by_barcode(barcode)
    if product is None:
        return jsonify({"error": f"Product {barcode} not found"}), 404
    return jsonify(product), 200

@app.route('/external/import/<barcode>', methods=['POST'])
def external_import_product(barcode):
    """Fetch a product from OpenFoodFacts and add it to inventory."""
    product = external_api.fetch_by_barcode(barcode)
    if product is None:
        return jsonify({"error": f"Product {barcode} not found"}), 404

    new_item = inventory.create({
        "product": product["product"],
        "price": 0.0,
        "stock": 0
    })
    return jsonify(new_item), 201

if __name__ == '__main__':
    app.run(debug=True)
