from app import app, db
from flask import jsonify, request, abort
from .models import Product, Offer
from .offer_microservice import OfferMicroservice
from sqlalchemy.exc import IntegrityError

@app.route('/')
def check():
    return "It works!"

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.to_collection_dict(Product.query.all())
    return jsonify(products)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product == None:
        abort(404)
    product = Product.to_collection_dict([product])
    return jsonify(product)

@app.route('/api/products', methods=['POST'])
def create_product():
    if not request.json or not 'name' in request.json:
        abort(400)
    new_product = {
        'name': request.json['name'],
        'description': request.json.get('description', "")
    }
    product = Product()
    product.from_dict(data=new_product)
    db.session.add(product)
    try:
        db.session.commit()
    except IntegrityError:
        abort(409)
    # zaregistrovat nový produkt
    data = product.to_dict()
    service = OfferMicroservice()
    service.register_new_product(data)
    response = jsonify(data)
    response.status_code = 201
    return response

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    if not request.json:
        abort(400)
    product = Product.query.get(product_id)
    if product == None:
        abort(404)
    data = {
        'name': request.json.get('name', product.name),
        'description': request.json.get('description', product.description)
    }
    product.from_dict(data=data)
    db.session.add(product)
    try:
        db.session.commit()
    except IntegrityError:
        abort(409)
        data = {
           'error': "Product with this name already exists",
        }
        response = jsonify(data)
        response.status_code = 409
        return response
    response = jsonify(product.to_dict())
    return response

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product == None:
        abort(404)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'result': True})


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request'}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(409)
def conflict(error):
    return jsonify({'error': 'Product with this name already exists'}), 409