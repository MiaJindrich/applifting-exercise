from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True, nullable=False)
    description = db.Column(db.String)
    offers = db.relationship('Offer', backref='product')

    def __repr__(self):
        return '<Product {}>'.format(self.name)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'description']:
            if field in data:
                setattr(self, field, data[field])

    def to_collection_dict(items):
        data = {
            'products': [item.to_dict() for item in items],
        }
        return data

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    items_in_stock = db.Column(db.Integer)
    external_offer_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __repr__(self):
        return '<Offer {}>'.format(self.id)

class AccessToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, nullable=False)
