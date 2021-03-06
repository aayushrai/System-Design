import pika,json,os,django
from pika import connection
from pika import channel
from main import Product, db

 # below 2 line added because this file is outside django app and we are using it without this django app throw an error
os.environ.setdefault("DJANGO_SETTING_MODULE","admin.settings") 
django.setup()

params = pika.URLParameters(
    "amqps://lrtmtglx:oYHJOduxC6B0WByra-d6Rzw0ge8R8sLY@hornet.rmq.cloudamqp.com/lrtmtglx")
connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.queue_declare(queue="main")


def callback(ch, method, properties, body):
    print("Received in main")
    data = json.loads(body)
    print(data)

    try:
        if properties.content_type == "product_created":
            product = Product(
                id=data["id"], title=data["title"], image=data["image"])
            db.session.add(product)
            db.session.commit()
            print("Product Created Successfully")

        elif properties.content_type == "product_updated":
            product = Product.query.get(data["id"])
            product.title = data["title"]
            product.image = data["image"]
            db.session.commit()
            print("Product Updated Successfully")

        elif properties.content_type == "product_deleted":
            product = Product.query.get(data)
            db.session.delete(product)
            db.session.commit()
            print("Product Deleted Successfully")
    except Exception as e:
        print("Error while updating database :", e)


channel.basic_consume(
    queue="main", on_message_callback=callback, auto_ack=True)
print("Started consuming")
channel.start_consuming()
channel.close()
