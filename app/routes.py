from app import app, db
from flask import jsonify, request
from .models import Product, Offer

@app.route('/')
def check():
    return "It works!"

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.to_collection_dict(Product.query.all())
    return jsonify(products)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.to_collection_dict([Product.query.get(product_id)])
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
    db.session.commit()
    # ... zaregistrovat nový produkt - zavolam si tu metodu register_new_project

    response = jsonify(product.to_dict())
    response.status_code = 201
    return response

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    data = {
        'name': request.json.get('name', product.name),
        'description': request.json.get('description', product.description)
    }
    product.from_dict(data=data)
    db.session.add(product)
    db.session.commit()
    response = jsonify(product.to_dict())
    return response

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'result': True})