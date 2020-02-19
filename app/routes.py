from app import app
from flask import jsonify
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
    pass'''