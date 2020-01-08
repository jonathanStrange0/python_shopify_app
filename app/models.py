from app import db

class Product(db.Model):
    gid = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128), index=True)
    variants = db.relationship('Variant', backref='variant',\
                            cascade='save-update, delete, delete-orphan')

class Variant(db.Model):
    gid = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128), index=True)
    product_gid = db.Column(db.String(64), db.ForeignKey('product.gid'))


class Customer(db.Model):
    gid = db.Column(db.String(64), primary_key=True)
    first_name = db.Column( db.String(64), index=True)
    last_name = db.Column( db.String(64), index=True)

class Order(db.Model):
    gid = db.Column(db.String(64), primary_key=True)
