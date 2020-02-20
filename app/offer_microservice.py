import requests
from flask import Flask
from app import db
from app.models import Product, Offer, AccessToken


class OfferMicroservice():

    def get_access_token(self):
        access_token = AccessToken.query.first()
        if access_token is not None:
            return access_token.token 
        response = requests.post('https://applifting-python-excercise-ms.herokuapp.com/api/v1/auth').json()
        access_token = response['access_token']
        model = AccessToken(token = access_token)
        db.session.add(model)
        db.session.commit()
        return access_token

    def fetch_data_from_api(self):
        products = Product.query.all()
        for product in products:
            headers = {'Bearer': self.get_access_token()}
            offers = requests.get('https://applifting-python-excercise-ms.herokuapp.com/api/v1/products/{}/offers'.format(product.id), headers=headers).json()
            for offer in offers:
                model = Offer(price=offer['price'], items_in_stock=offer['items_in_stock'], external_offer_id=offer['id'], product=product)
                db.session.add(model)
                db.session.commit()
        '''
        získá všechny produkty z db
        z ms zavolám všechny offers na každý jeden produkt, jednotlivé offers projdu, přiřadím k nim atributy, produkt a uložím si je do db

        '''

    def register_new_product():
        