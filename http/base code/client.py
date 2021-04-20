import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import base64
import requests

def create_request_to_ai_engine(engine,jpg_as_text,frame_no,group):
    try:
        requests.post(engine, data = {"image":jpg_as_text,"frame_no":frame_no,"group":group})
    except Exception as e:
        print("Error while sending frame to ai engine")
  
engines  = ["http://127.0.0.1:6001","http://127.0.0.1:6002","http://127.0.0.1:6003","http://127.0.0.1:6004"]      
engineCounter = 0
group = "a"
      
cam = cv2.VideoCapture(0)

# cam.set(3, 320);
# cam.set(4, 240);

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cam.read()
    retval, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer) 
    
    if engineCounter >= 4:
        engineCounter = 0
        group = ord(group) + 1
        group = chr(group)
    
    if group > "z":
        group = "a"
   
    # engineCounter += 1
    

    if engineCounter >= 4:
        engineCounter = 0
    # print("{}: {}".format(img_counter, size))
    st = time.time()
    create_request_to_ai_engine(engines[engineCounter],jpg_as_text,img_counter,group)
    print("time taken",time.time()-st)
    engineCounter += 1
    img_counter += 1

cam.release()