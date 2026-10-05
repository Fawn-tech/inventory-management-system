from flask import Flask, jsonify, request
import inventory

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

if __name__ == '__main__':
    app.run(debug=True)
