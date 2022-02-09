import pika, json

params = pika.URLParameters('amqps://tlontitk:MNGLzB3rtgSA-__gGASK-9oGNs2PSbKC@lionfish.rmq.cloudamqp.com/tlontitk')
connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    # channel.basic_publish(exchange='', routing_key='admin', body='hello')
    properties = pika.BasicProperties(method)
    # channel.basic_publish(exchange='', routing_key='main', body='hello from main')
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)

