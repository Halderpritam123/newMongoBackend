from bson.objectid import ObjectId
from flask_pymongo import PyMongo

mongo = PyMongo()


class Dish:
    collection_name = 'dishes'

    def __init__(self, name, price, availability):
        self.name = name
        self.price = price
        self.availability = availability

    @staticmethod
    def get_all_dishes():
        dishes = mongo.db[Dish.collection_name].find()
        result = []
        for dish in dishes:
            result.append({
                'dish_id': str(dish['_id']),
                'dish_name': dish['name'],
                'price': dish['price'],
                'availability': dish['availability']
            })
        return result

    def save(self):
        dish = {
            'name': self.name,
            'price': self.price,
            'availability': self.availability
        }
        inserted_dish = mongo.db[Dish.collection_name].insert_one(dish)
        return str(inserted_dish.inserted_id)

    @staticmethod
    def update_availability(dish_id, availability):
        mongo.db[Dish.collection_name].update_one({'_id': ObjectId(dish_id)},
                                                 {'$set': {'availability': availability}})

    @staticmethod
    def delete_dish(dish_id):
        mongo.db[Dish.collection_name].delete_one({'_id': ObjectId(dish_id)})
