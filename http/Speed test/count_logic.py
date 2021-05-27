from flask import Flask, request
import base64
import threading
import requests

app = Flask(__name__)

frames = {}

@app.route("/", methods=["POST"])
def home():
    result = request.form.get("result")
    service = request.form.get("service")
    group = request.form.get("group")
    
    if group not in frames:
        frames[group] = [result]
    else:
        frames[group].append(result)
    
    if frames[group] == 4:
        # ========code=========
        del frames[group]
        
    # t1 = threading.Thread(target=face_r.get_frame,args=[frame,camera_name,camera_url,timestamp,service])
    # t1.start()
    # # face_r.get_frame(frame,camera_name,camera_url,timestamp,service)
    return 'Success!'   

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True,port="6000",threaded=True)