import pika
from pika import connection
from pika import channel
import json

params = pika.URLParameters(
    "amqps://lrtmtglx:oYHJOduxC6B0WByra-d6Rzw0ge8R8sLY@hornet.rmq.cloudamqp.com/lrtmtglx")
connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange="", routing_key="main",
                          body=json.dumps(body), properties=properties)
