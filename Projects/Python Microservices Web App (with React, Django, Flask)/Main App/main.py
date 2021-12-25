from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint

app = Flask(__name__)   # creating flask app
app.config["SQLALCHEMY_DATABASE_URL"] = "mysql://root:root@db/main" # for data base connection mysql://user:password@host/database
CORS(app)  # adding cors

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=False)  # we turn off the auto increment because we are going to use product_id which is coming from django
    title = db.Column(db.String(200))
    image = db.Column(db.String(200)) 

class ProductUser(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint("user_id","product_id",name="user_product_unique")



@app.route("/")
def index():
    return "Hello world"


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")