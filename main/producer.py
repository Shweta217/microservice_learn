import pika, json

params = pika.URLParameters('amqps://tlontitk:MNGLzB3rtgSA-__gGASK-9oGNs2PSbKC@lionfish.rmq.cloudamqp.com/tlontitk')
connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)

