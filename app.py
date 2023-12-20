from food import Food, FoodQuery, Foods

from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

server = Flask(__name__)

spec = FlaskPydanticSpec('flask', title="Food API")
spec.register(server)

database = TinyDB(storage=MemoryStorage)

@server.get('/foods')
@spec.validate(query=FoodQuery, resp=Response(HTTP_200=Foods))
def get_foods():
    """Get foods from the database"""
    food_query = Query()
    filters_query = request.context.query.dict(exclude_none=True)
    
    result = database.search(food_query.fragment(filters_query))
    
    if(result):
        return jsonify(
            Foods(foods = result,
            count = len(result)).dict()
        )    
        
    return {"error": "Foods not found"}, 404
    
@server.get('/food/<int:id>')
@spec.validate(resp=Response(HTTP_200=Food))
def get_food(id):
    """Get a especific food from the database"""
    food_query = Query()
    
    result = database.search(food_query.id == id)
    
    if result:
        return jsonify(result[0])
    
    return {"error": "Food not found"}, 404

@server.post('/food')
@spec.validate(body=Request(Food), resp=Response(HTTP_201=Food))
def post_food():
    """Inserts a food into the database"""
    body = request.context.body.dict()
    
    database.insert(body)
     
    return body

@server.put('/food/<int:id>')
@spec.validate(body=Request(Food), resp=Response(HTTP_200=Food))
def put_food(id):
    """Update a food into the database"""
    food_query = Query()
    
    body = request.context.body.dict()
    body.pop('id', None)
    body['id'] = id
    
    database.update(body, food_query.id == id)
    
    return jsonify(body)

@server.delete('/food/<int:id>')
@spec.validate(resp=Response('HTTP_204'))
def delete_food(id):
    """Delete a food into the database"""
    food_query = Query()
    
    database.remove(food_query.id == id)
    
    return jsonify({})

if __name__ == '__main__':
    server.run()