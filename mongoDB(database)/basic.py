from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient("mongodb+srv://admin:facegenie@cluster0.cthw8.mongodb.net/facegenie?retryWrites=true&w=majority")
print(client)
db=client.facegenie # facegenie is database 
print(db)
mycol = db.cloudFirestore #cloudFirestore is collection (it's like table in rdbms)


for doc in mycol.find():    # doc is document in collection (it's like row in rdbms)
    pprint(doc)

# https://realpython.com/introduction-to-mongodb-and-python/