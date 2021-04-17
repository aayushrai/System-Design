
import cv2
import io
import socket
import struct
import time
import pickle
import zlib

engines  = []      
engineCounter = 0

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 6000))
connection = client_socket.makefile('wb')
engines.append(client_socket)

client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket1.connect(('127.0.0.1', 6001))
connection1 = client_socket1.makefile('wb')
engines.append(client_socket1)

client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket2.connect(('127.0.0.1', 6002))
connection2 = client_socket2.makefile('wb')
engines.append(client_socket2)

client_socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket3.connect(('127.0.0.1', 6003))
connection3 = client_socket3.makefile('wb')
engines.append(client_socket3)


cam = cv2.VideoCapture(0)

# cam.set(3, 320);
# cam.set(4, 240);

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    frame_no = img_counter
    group = 'a'
#    data = zlib.compress(pickle.dumps(frame, 0))
    data = pickle.dumps([frame,frame_no,group], 0)
    size = len(data)

    if engineCounter >= 4:
        engineCounter = 0
    # print("{}: {}".format(img_counter, size))
    st = time.time()
    try:
        engines[engineCounter].sendall(struct.pack(">L", size) + data)
    except Exception as e:
        print(e)
        print("May be socket ",engineCounter,"not running")
    print("time taken",time.time()-st)
    engineCounter += 1
    img_counter += 1

cam.release()