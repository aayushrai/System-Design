import redis
from datetime import datetime
from threading import Thread
 #Create a redis client
import logging

logging.basicConfig(filename="test.log", level=logging.DEBUG)


class Pipelines(object):
    def __init__(self,host='localhost',port=6379,db=5,passsword=None,socket_timeout=10):
        self.host = host
        self.port = port
        self.db = db
        self.passsword = passsword
        self.socket_timeout = socket_timeout
        self.conn=self.__connect__()
        self.data={}
    
    def __connect__(self):
        '''
           connect to redis server 
        '''
        try:
            conn = redis.Redis(host=self.host,port= 6379,password=self.passsword,db=self.db)
            print("Connection sucessfull...")
        except redis.RedisError as rerror:
            print("Connection Error with redis error {}".format(rerror))
        return conn
    

   
    def __data__(self,data):
        '''
            function append data to be send to pileline
            Note data size min max 8 mb to 10 mb
        '''
        self.data=data
        return self.data

    def push(self,channel_name):
        try:
            self.conn.publish(channel_name,str(self.data))
        except Exception.RedisError as er:
            print("Raside exception error {}".format(er))
        
    def publisher(self,data,channel_name):
        '''
        this is main function to run publisher function
        publish message 
        '''
        strat_time=datetime.now()
        print("data size {}".format(len(data)))
        for i in range(len(data)):
            #self.conn.lpush('data',data[i])
        
            self.data=self.__data__(data[i])
            try:
                self.conn.publish(channel_name,str(self.data))
            except Exception.RedisError as er:
                print ("Exceptions raised {}".format(er))
            #print("Date time {}".format(datetime.now()))
        end_time=datetime.now()
        print("elapse time = {} \n start_tme = {}  sent \n time = {}".format(end_time-strat_time,strat_time,end_time))

#test cases for publisher function


threads=[]


from faker import Faker

fake= Faker('en_US')
data=[]
for i in range(25000):
    d={"first_name":fake.first_name(),'name':fake.name() }
    data.append(d)



'''
This program test publisher subscriber artitecture to send 10 randlom user's data to the redis server
 

'''



if __name__ == '__main__':
    strat_time = datetime.now() 
    for i in range(42):                   # 42 different publisher
        worker= Pipelines(host='localhost',port=6379,db=5,passsword=None,socket_timeout=10)  # each publisher publish 25000 messages
        #worker.publisher,args=(25000,,)
        threads.append(Thread(name='''id_'''+str(i),target=worker.publisher,args=(data,'json_loader',)))

    for thread in threads:
        thread.start()
        thread.join()
   
    print("All process done")
    end_time = datetime.now()
    estimatedTime=(end_time-strat_time)




