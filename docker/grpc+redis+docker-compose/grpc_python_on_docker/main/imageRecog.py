import numpy as np 
import base64       
# import face_recognition
import os
import joblib
import redis
from datetime import datetime
import logging
import json
logging.basicConfig(filename="test.log", level=logging.DEBUG)


base_dir=os.path.dirname(os.path.realpath(__file__))
loaded_model = joblib.load(os.path.join(base_dir,"cam_ai_cache.sav"))


# Redis write back strategy
class Pipelines(object):
    def __init__(self,host='redis',port=6379,db=5,passsword=None,socket_timeout=10):
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
            print("Redis Connection Establish successfully...")
            print("Don't forget to start redis server")
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
        try:
            self.conn.publish(channel_name,data)
        except Exception.RedisError as er:
            print ("Exceptions raised {}".format(er))
        #print("Date time {}".format(datetime.now()))
        end_time=datetime.now()
        print("time taken",end_time-strat_time)

worker= Pipelines(host='redis',port=6379,db=5,passsword=None,socket_timeout=10)

# def reogniser(frame):
# 	all_names =[]
# 	face_locations = face_recognition.face_locations(frame)
# 	no = len(face_locations)
# 	if no >= 1:
# 		print("Number of faces detected: ", no)

# 		# Predict all the faces in the test image using the trained classifier
# 		print("Found:")
# 		for i in range(no):
# 			test_image_enc = face_recognition.face_encodings(frame)[i]
# 			name = loaded_model.predict([test_image_enc])
# 			all_names.extend(name)
			
# 		return all_names
# 	else:
# 		return all_names

def publishDataToRedis(user_ids):
	attendees = []
	for user_id in user_ids:
		print(user_id)
		attendees.append(
			{
				"camera_name": "1",
				"date" : "",
				"result" : {
					"uid": user_id,
					"mask_status":False
				},
				"service" : "attendance",
				"time" : ""
			}
		)
	worker.publisher(json.dumps(attendees),'json_loader')
	#worker.publisher,args=(25000,,)
	# Thread(name='''id_'''+str(i),target=worker.publisher,args=(data,'json_loader',))


def faceRecogAndPublishToRedis(imgarr):
    # user_ids = reogniser(imgarr)
    user_ids = ["aauidfjdklfjkffklfThisidcreatedbyme"]
    print(user_ids)
    try:
        publishDataToRedis(user_ids)
    except:
        print("Error while publishing data on redis")
        
def FaceRecog(b64img_compressed, w, h):
    b64decoded = base64.b64decode(b64img_compressed)
    decompressed = b64decoded #zlib.decompress(b64decoded)
    imgarr = np.frombuffer(decompressed, dtype=np.uint8).reshape(w, h, -1)
    faceRecogAndPublishToRedis(imgarr)
    return "success"
