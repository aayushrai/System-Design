
import threading
import requests
import socket
import pickle
import struct


HOST= '127.0.0.1' 

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,7000))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
connected = set()

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
    frame_no,group,roi = frameAndMsg
    print(frameAndMsg)
    print("frame number",frame_no)
    print("grp" , group)

