# -*- coding: utf-8 -*-
"""
@author: shotaro27
"""

import cv2
import os
import glob
import csv
import re
from detector_lib import landmark_detector

dir_path = os.path.dirname(__file__)

pictures_path = os.path.join(dir_path,"sample_datas")
output_path = os.path.join(dir_path,"outputs\\output.csv")
test_output_path = os.path.join(dir_path,"outputs\\test_output.csv")

def ascending_order(text):
    return [ int(t) if t.isdigit() else t for t in re.split(r'(\d+)', text) ]

units = sorted(glob.glob(pictures_path + "\\*"), key=ascending_order)

outputs = []
test_outputs = []

for unit in units:
    data_sets = sorted(glob.glob(unit + "\\*"))
    print(unit)
    for i, data_set in enumerate(data_sets):
        #補正用の画像のみ分離
        init = glob.glob(data_set + "\\init*.jpg")
        pictures = glob.glob(data_set + "\\*.jpg")
        pictures.remove(init[0])
        print(init[0])

        #補正値の検出
        frame = cv2.imread(init[0])
        init_detector = landmark_detector(frame)
        if not hasattr(init_detector, 'cx_iris_r'): continue
        
        for picture_path in pictures:
            #特徴点検出
            frame = cv2.imread(picture_path)
            detector = landmark_detector(frame)
            if not hasattr(detector, 'cx_iris_r'): continue

            #正解データ
            picture_name = os.path.basename(picture_path)
            name_split = re.split("[_\.\(\)]", picture_name)
            answer_x = name_split[1]
            answer_y = name_split[2]

            #出力
            output = detector.output()
            output.append(init_detector.correction_x)
            output.append(init_detector.correction_y)

            output.append(answer_x)
            output.append(answer_y)

            if i == 3:
                test_outputs.append(output)
            else:
                outputs.append(output)
        
#出力データをCSV形式で書き出し
with open(output_path, 'a', newline="") as f:
    writer = csv.writer(f)
    for output in outputs:
        writer.writerow(output)

with open(test_output_path, 'a', newline="") as f:
    writer = csv.writer(f)
    for test_output in test_outputs:
        writer.writerow(test_output)
