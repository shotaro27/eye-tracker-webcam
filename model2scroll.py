# -*- coding: utf-8 -*-
"""
@author: shotaro27
"""

import cv2
import os
import pyautogui as pgui
import pickle
from detector_lib import landmark_detector
pgui.FAILSAFE=False

dir_path = os.path.dirname(__file__)

model1_path = os.path.join(dir_path,"model\\model1.pickle")
model2_path = os.path.join(dir_path,"model\\model2.pickle")

with open(model1_path, mode='rb') as f:
    model1 = pickle.load(f)

with open(model2_path, mode='rb') as f:
    model2 = pickle.load(f)

cap = cv2.VideoCapture(0)

while (True):
    ret,frame = cap.read()
    detector = landmark_detector(frame);
    cv2.imshow("frame", frame)
    
    k = cv2.waitKey(1) & 0xFF
    
    if hasattr(detector, 'cx_iris_r'):
        x_list = detector.output()
        c1, c2 = detector.get_correction()
        x_list.append(c1)
        x_list.append(c2)
        
        #式
        y_pred_y1 = model1.predict([x_list])#座標
        y_pred_y2 = model2.predict([x_list])
        
        result_x = y_pred_y1[0]
        result_y = y_pred_y2[0]
        
        #スクロール
        d_size = pgui.size()
        speed = 5
        scroll_x = (-int((result_x - 40) * speed)
            if result_x < 40 else -int((result_x - 60) * speed)
            if result_x > 60 else 0)
        scroll_y = (-int((result_y - 40) * speed)
            if result_y < 40 else -int((result_y - 60) * speed)
            if result_y > 60 else 0)
        # scroll_y = -int((result_y - 50) * speed)
        pgui.hscroll(scroll_x)
        pgui.scroll(scroll_y)
        print(result_y)
        
    if  k == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()