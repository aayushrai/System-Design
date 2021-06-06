import redis

 #Create a redis client
from datetime import datetime


class Redis_SUBS(object):
    def __init__(self,host="localhost",port= 6379,password=None, db=0,socket_timeout=10):
        self.conn=redis.Redis(host=host,port= port,password=password,db=db)


    def listener(self,pubsub):
        count = 0
        while True:
            for item in pubsub.listen():
                
                #self.conn.lpush('response',str(item))
                print("Message  {}".format(count))
                count += 1
                print(datetime.now())
                
            if count >= 55000:
                break
        return False
    def run(self,channels):
        pubsub=self.conn.pubsub()
        
        while True:
            pubsub.subscribe(channels)
            listeners= self.listener(pubsub)
            if listeners == False:
                pubsub.unsubscribe()

                print("Subscribing............. \n")
        return 1
            
d=Redis_SUBS(host="localhost",port= 6379,password=None,db=5)

d.run(["json_loader"])