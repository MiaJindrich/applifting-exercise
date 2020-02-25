import os
import requests
import tempfile
import pytest
import random
from .config import Config
from app.models import Product

base_url = "http://127.0.0.1:5000/api/"

def test_get_products():
    url = base_url + 'products'
    assert requests.get(url).status_code == 200

def test_create_product():
    data = {"name": "Testovací produkt" + str(random.choice for i in range(1000)), "description": "Popis testovacího produktu"}
    response = requests.post(base_url + 'products', json=data)
    assert response.status_code == 201 or response.status_code == 409
    
    response = requests.post(base_url + 'products', json=data)
    assert response.status_code == 409

def test_get_product():
    data = {"name": "Testovací produkt" + str(random.choice for i in range(1000)), "description": "Popis testovacího produktu"}
    response = requests.post(base_url + 'products', json=data)
    assert response.status_code == 201

    id = response.json()['id']

    response = requests.get(base_url + 'products/' + str(id))
    assert response.status_code == 200
    assert 'products' in response.json()

def test_update_product():
    data = {"name": "Testovací produkt" + str(random.choice for i in range(1000)), "description": "Popis testovacího produktu"}
    response = requests.post(base_url + 'products', json=data)
    assert response.status_code == 201

    id = response.json()['id']

    response = requests.put(base_url + 'products/' + str(id), json={"name": "Nový název"})
    assert response.status_code == 200 or response.status_code == 409
    if response.status_code == 200:
        assert 'Nový název' == response.json()['name']

def test_delete_product():
    data = {"name": "Testovací produkt" + str(random.choice for i in range(1000)), "description": "Popis testovacího produktu"}
    response = requests.post(base_url + 'products', json=data)
    assert response.status_code == 201

    id = response.json()['id']

    response = requests.delete(base_url + 'products/' + str(id), json=data)
    assert response.status_code == 200
