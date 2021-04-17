from flask import Flask, request
import base64
import threading
import requests

app = Flask(__name__)


countLogicUrl = ""

def create_request_to_count_logic(jpg_as_text,frame_no,service,group):
    global countLogicUrl
    try:
        requests.post(countLogicUrl, data = {"result":result,,"service":service,"group":group})
    except Exception as e:
        print("Error while sending ressult to counter logic")
        
@app.route("/", methods=["POST"])
def home():
    img = request.form.get("image")
    service = request.form.get("service")
    frame_no = request.form.get("frame_no")
    group = request.form.get("group")
    jpg_original = base64.b64decode(img)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    frame = cv2.imdecode(jpg_as_np, flags=1)
    # t1 = threading.Thread(target=face_r.get_frame,args=[frame,camera_name,camera_url,timestamp,service])
    # t1.start()
    # # face_r.get_frame(frame,camera_name,camera_url,timestamp,service)
    return 'Success!'   

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True,port="6000",threaded=True)