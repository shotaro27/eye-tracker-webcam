import cgi

# デバッグ用
import cgitb
cgitb.enable()

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from detector_lib import landmark_detector
import base64
import numpy as np
import cv2
import re

print ("Content-Type: text/html")
print()
    
def detect(frame):
    detector = landmark_detector(frame);
    if hasattr(detector, 'cx_iris_r'):
        correction_x = (detector.cx_iris_r - detector.cx_iris_l) / 2
        correction_y = (detector.cy_iris_r + detector.cy_iris_l) / 2
        return correction_x, correction_y
    else: return 0, 0
        
print ("<html><body>")

form = cgi.FieldStorage()
form_check = 0

b64data = re.split(",", form["pic"].value)[1]
img_binary = base64.b64decode(b64data)
jpg=np.frombuffer(img_binary,dtype=np.uint8)
img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)
c1, c2 = detect(img);
print("c1 = {}<br>".format(c1))
print("c2 = {}<br>".format(c2))
print ("</body></html>")