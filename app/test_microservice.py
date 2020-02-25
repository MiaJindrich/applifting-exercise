import pytest
import requests
import random
from .offer_microservice import OfferMicroservice
from .models import Product

service = OfferMicroservice()
def test_get_access_token():
    assert len(service.get_access_token()) > 1

def test_register_new_product():
    data = {"id": (random.choice for i in range(1000)), "name": "Testovací produkt" + str(random.choice for i in range(1000)), "description": "Popis testovacího produktu"}
    response = service.register_new_product(data)
    assert response == True
