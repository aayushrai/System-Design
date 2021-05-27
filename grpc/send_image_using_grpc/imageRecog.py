import numpy as np 
import base64
import zlib
import cv2

def FaceRecog(b64img_compressed, w, h):
    b64decoded = base64.b64decode(b64img_compressed)

    decompressed = b64decoded #zlib.decompress(b64decoded)

    imgarr = np.frombuffer(decompressed, dtype=np.uint8).reshape(w, h, -1)
    
    cv2.imwrite("aayush.jpg",imgarr)
    return "aayush"