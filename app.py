from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
from config import MONGO_URI

app = Flask(__name__)
CORS(app) 

app.config["MONGO_URI"] = MONGO_URI

mongo = PyMongo(app)


# Route to retrieve all dishes
@app.route('/dishes', methods=['GET'])
def get_all_dishes():
    dishes = mongo.db.dishes.find()
    result = []
    for dish in dishes:
        result.append({
            'dish_id': str(dish['_id']),
            'dish_name': dish['name'],
            'price': dish['price'],
            'availability': dish['availability']
        })
    return jsonify(result)


# Route to add a new dish
@app.route('/dishes', methods=['POST'])
def add_dish():
    data = request.json
    dish = {
        'name': data['name'],
        'price': data['price'],
        'availability': data['availability']
    }
    inserted_dish = mongo.db.dishes.insert_one(dish)
    return jsonify({'dish_id': str(inserted_dish.inserted_id)})


# Route to update the availability of a dish
@app.route('/dishes/<dish_id>', methods=['PUT'])
def update_dish_availability(dish_id):
    data = request.json
    updated_dish = mongo.db.dishes.update_one({'_id': ObjectId(dish_id)}, {'$set': {'availability': data['availability']}})
    return jsonify({'success': True})


# Route to delete a dish
@app.route('/dishes/<dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    mongo.db.dishes.delete_one({'_id': ObjectId(dish_id)})
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run()