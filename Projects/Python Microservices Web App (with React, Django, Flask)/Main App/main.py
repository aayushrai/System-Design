from flask import Flask,jsonify,abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint
from dataclasses import dataclass
import requests
from producer import publish

app = Flask(__name__)   # creating flask app

# for data base connection mysql://user:password@host/database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@db/main"
CORS(app)  # adding cors

db = SQLAlchemy(app)

@dataclass
class Product(db.Model):
    # we turn off the auto increment because we are going to use product_id which is coming from django
    id: int
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

    UniqueConstraint("user_id", "product_id", name="user_product_unique")


@app.route("/api/products")
def index():
    return jsonify(Product.query.all())

@app.route("/api/products/<int:product_id>/like", methods=["POST"])
def like(product_id):
    # req = requests.get("http://docker.for.linux.localhost:8000/api/user")    # here we are taking random user for liked post
    # json = req.json()
    print("aaaa",product_id)
    try:
        productUser = ProductUser(user_id=1, product_id=product_id)
        db.session.add(productUser)
        db.session.commit()

        publish("product_liked", product_id)
    except:
        abort(400, "You already liked this product")

    return jsonify({
        "message": "success"
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
