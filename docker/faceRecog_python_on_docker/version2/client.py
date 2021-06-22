import requests
import cv2
import base64
import json
img = cv2.imread("aayush.jpg")
retval, buffer = cv2.imencode('aayush.jpg', img)

# Convert to base64 encoding and show start of data
jpg_as_text = base64.b64encode(buffer)

url = "http://0.0.0.0:5000/facerecog"
x = requests.post(url, data = {"image":jpg_as_text})
print(x.text)
url = "http://0.0.0.0:5000/registration"
x = requests.post(url, data = {"image":jpg_as_text,"id":"232323"})
print(x.text)