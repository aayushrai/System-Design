import pika
from pika import connection
from pika import channel

params = pika.URLParameters("amqps://lrtmtglx:oYHJOduxC6B0WByra-d6Rzw0ge8R8sLY@hornet.rmq.cloudamqp.com/lrtmtglx")
connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish():
    channel.basic_publish(exchange="",routing_key="main",body="hello")