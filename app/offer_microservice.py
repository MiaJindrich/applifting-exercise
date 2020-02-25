import requests
from flask import Flask
from app import db
from .models import Product, Offer, AccessToken


class OfferMicroservice():
    def __init__(self, base_url=None):
        self.base_url = base_url or "https://applifting-python-excercise-ms.herokuapp.com/api/v1"

    def get_access_token(self):
        access_token = AccessToken.query.first()
        if access_token is not None:
            return access_token.token 
        response = requests.post(self.base_url + '/auth').json()
        access_token = response['access_token']
        model = AccessToken(token = access_token)
        db.session.add(model)
        db.session.commit()
        return access_token

    def fetch_data_from_api(self):
        # calls all products, gets offers from each of them, saves them to database
        products = Product.query.all()
        for product in products:
            headers = {'Bearer': self.get_access_token()}
            offers = requests.get(self.base_url + '/products/{}/offers'.format(product.id), headers=headers).json()
            for offer in offers:
                model = Offer(price=offer['price'], items_in_stock=offer['items_in_stock'], external_offer_id=offer['id'], product=product)
                db.session.add(model)
                db.session.commit()

    def register_new_product(self, product):
        headers = {'Bearer': self.get_access_token()}
        response = requests.post(self.base_url + '/products/register', data=product, headers=headers)
        if response.status_code == 201:
            return True
        else:
            return False
        