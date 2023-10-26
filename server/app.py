#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    name = request.form.get('name')
    price = request.form.get('price')
    bakery_id = request.form.get('bakery_id')

    if not name or not price or not bakery_id:
        # Handle validation error
        return make_response(jsonify({'error': 'Missing data'}), 400)

    # Create a new baked good in the database
    new_baked_good = BakedGood(name=name, price=price, bakery_id=bakery_id)
    db.session.add(new_baked_good)
    db.session.commit()

    # Return the created baked good as JSON
    return jsonify({
        'id': new_baked_good.id,
        'name': new_baked_good.name,
        'price': new_baked_good.price,
        'bakery_id': new_baked_good.bakery_id
    }), 201
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def bakery_by_id(id):
    new_name = request.form.get('name')

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()
    
    bakery.name = new_name
    db.session.commit()


    response = make_response(
        bakery_serialized,
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    # Find the baked good by ID
    baked_good = BakedGood.query.get(id)
    
    # Delete the baked good from the database
    db.session.delete(baked_good)
    db.session.commit()

    # Return a JSON response confirming the deletion
    return jsonify({'message': 'Baked good deleted'})

if __name__ == '__main__':
    app.run(port=5555, debug=True)
