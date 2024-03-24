from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

# Configure MongoDB URI
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ruse_db'

# Initialize PyMongo
mongo = PyMongo(app)

# Sample route to test if Flask is running
@app.route('/')
def hello():
    return jsonify(message="Hello, Ruse!")

# Route to add a new device
@app.route('/devices', methods=['POST'])
def add_device():
    data = request.json
    if data:
        inserted_id = mongo.db.devices.insert_one(data).inserted_id
        return jsonify(message="Device added successfully", _id=str(inserted_id))
    else:
        return jsonify(error="No data provided"), 400

# Route to update a device
@app.route('/devices/<string:device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.json
    if data:
        result = mongo.db.devices.update_one({'_id': ObjectId(device_id)}, {'$set': data})
        if result.modified_count > 0:
            return jsonify(message="Device updated successfully")
        else:
            return jsonify(error="Device not found"), 404
    else:
        return jsonify(error="No data provided"), 400

# Route to delete a device
@app.route('/devices/<string:device_id>', methods=['DELETE'])
def delete_device(device_id):
    result = mongo.db.devices.delete_one({'_id': ObjectId(device_id)})
    if result.deleted_count > 0:
        return jsonify(message="Device deleted successfully")
    else:
        return jsonify(error="Device not found"), 404

if __name__ == '__main__':
    app.run(debug=True)