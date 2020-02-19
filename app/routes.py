from app import app, db
from flask import jsonify, request
from .models import Product, Offer

@app.route('/')
def check():
    return "It works!"

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify({'products': products})

'''@app.route('/api/products/<int:product_id', methods=['GET'])
def get_product(product_id):
    '''

@app.route('/api/products', methods=['POST'])
def create_product():
    if not request.json or not 'name' in request.json:
        abort(400)
    new_product = {
        'name': request.json['name'],
        'description': request.json.get('description', "")
    }
    product = Product()
    product.from_dict(data=new_product, new_product=True)
    db.session.add(product)
    db.session.commit()
    response = jsonify(product.to_dict())
    response.status_code = 201
    return response