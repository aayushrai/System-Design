import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib

# connecting socket with count logic
count_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
count_socket.connect(('127.0.0.1', 7000))
connection = count_socket.makefile('wb')



# creating socket for ai engine
HOST= '127.0.0.1' 
# PORT=8000
PORT =int(sys.argv[1])
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')
s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')
conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))


def send_roi_to_count_logic():
    global count_socket
    data = pickle.dumps([PORT,"a",[3423,324324,324]], 0)
    size = len(data)
    count_socket.sendall(struct.pack(">L", size) + data)
    
while True:   

    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += conn.recv(409600)
    
    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(409600)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frameAndMsg=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame,frame_no,group = frameAndMsg[0],frameAndMsg[1],frameAndMsg[2]
    print("frame number",frame_no)
    print("grp" , group)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    resize = cv2.resize(frame,(500,500))
    send_roi_to_count_logic()
    # cv2.imshow('ImageWindow',resize)
    # cv2.waitKey(1)