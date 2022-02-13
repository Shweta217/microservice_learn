from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from dataclasses import dataclass
import requests
# from producer import publish
import pika, json

params = pika.URLParameters('amqps://tlontitk:MNGLzB3rtgSA-__gGASK-9oGNs2PSbKC@lionfish.rmq.cloudamqp.com/tlontitk')
connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    # channel.basic_publish(exchange='', routing_key='admin', body='hello')
    properties = pika.BasicProperties(method)
    # channel.basic_publish(exchange='', routing_key='main', body='hello from main')
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://admin:rootpass@product-db-1.c6prxrox2sgw.ap-south-1.rds.amazonaws.com/main'
CORS(app)

db = SQLAlchemy(app)

@dataclass
class Product(db.Model):
    id : int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')

# @app.route('/')
@app.route('/api/products')
def index():
  # return "Hello"
  return jsonify(Product.query.all())

@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://13.234.128.148:8000/api/user')
    json = req.json()
    # return jsonify(req.json())
    try:
       productUser = ProductUser(user_id=json['id'], product_id=id)
       db.session.add(productUser)
       db.session.commit()
       publish('product_liked', id)
    # event
    except:
       abort(400, 'You already liked this product')
    return jsonify({'message' : 'success'})

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')  
