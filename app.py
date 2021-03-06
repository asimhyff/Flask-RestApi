from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# DataBase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACKER_MODIFICATION'] = False

# init db
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)

# Product class/model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

# product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')

# init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True) 

# create Product
@app.route('/addproduct', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)
    
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# show all products
@app.route('/showallproducts' , methods=['GET'])
def get_all_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# get by id
@app.route('/product/<id>', methods=['GET'])
def get_product_by_id(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


# Update a product

@app.route('/updateproduct/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()

    return product_schema.jsonify(product)


# delete a product
@app.route('/deleteproductbyid/<id>', methods=['DELETE'])
def delete_by_id(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    
    return product_schema.jsonify(product)


#Run server
if __name__ == '__main__':
    app.run(debug=True)