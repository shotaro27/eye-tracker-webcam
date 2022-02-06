# -*- coding: utf-8 -*-
"""
@author: shotaro27
"""

import cv2
import os
import dlib
import configparser
from imutils import face_utils

class landmark_detector:
    dir_path = os.path.dirname(__file__)

    config_ini = configparser.ConfigParser()
    config_ini.read(os.path.join(dir_path, 'config.ini'), encoding='utf-8')
    
    def p_tile_threshold(self, img_gry, per):
        """
        Pタイル法による2値化処理
        :param img_gry: 2値化対象のグレースケール画像
        :param per: 2値化対象が画像で占める割合
        :return img_thr: 2値化した画像
        """

        # ヒストグラム取得
        img_hist = cv2.calcHist([img_gry], [0], None, [256], [0, 256])

        # 2値化対象が画像で占める割合から画素数を計算
        all_pic = img_gry.shape[0] * img_gry.shape[1]
        pic_per = all_pic * per

        # Pタイル法による2値化のしきい値計算
        p_tile_thr = 0
        pic_sum = 0

        # 現在の輝度と輝度の合計(高い値順に足す)の計算
        for hist in img_hist:
            pic_sum += hist

            # 輝度の合計が定めた割合を超えた場合処理終了
            if pic_sum > pic_per:
                break

            p_tile_thr += 1

        # Pタイル法によって取得したしきい値で2値化処理
        ret, img_thr = cv2.threshold(img_gry, p_tile_thr, 255, cv2.THRESH_BINARY_INV)

        return img_thr

    iris = {'center': (0, 0), 'radius': 0}

    def _detect_iris(self, eye_img):
        """
        2値化処理を利用した虹彩の測定
        :param eye_img: 目のグレースケール画像
        :return max_cnt: 虹彩の輪郭
        """
        eye_img_gau = cv2.GaussianBlur(eye_img, (1, 1), 0)

        global eye_img_thr
        eye_img_thr = self.p_tile_threshold(eye_img_gau,0.4)

        contours, hierarchy = cv2.findContours(eye_img_thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        max_cnt = max(contours,key = lambda x: cv2.contourArea(x))
        return max_cnt

    #顔認識オブジェクト
    face_detector = dlib.get_frontal_face_detector()
    predictor_path = os.path.join(dir_path,"shape_predictor_68_face_landmarks.dat")
    face_predictor = dlib.shape_predictor(predictor_path)

    def __init__(self, frame):
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        
        #顔認識
        faces = self.face_detector(gray, 1)
        
        if len(faces) == 0:
            return
        
        landmarks = []
        
        for face in faces:
            #顔の特徴点を検出
            landmark = self.face_predictor(gray, face)
            landmark = face_utils.shape_to_np(landmark)
            landmarks.append(landmark)
        
        #一番大きい顔を検出
        landmarks.sort(key=lambda x: x[0][0] - x[16][0])
        landmark = landmarks[0]
        
        #右目の座標取得
        right_eye_region = {'top_x': landmark[36][0], 'bottom_x': landmark[39][0],
            'top_y': landmark[37][1]
            if landmark[37][1] < landmark[38][1] else landmark[38][1],
            'bottom_y': landmark[41][1]
            if landmark[41][1] > landmark[40][1] else landmark[40][1]}
        right_eye = gray[right_eye_region["top_y"]:right_eye_region["bottom_y"],right_eye_region["top_x"]:right_eye_region["bottom_x"]]
        self.cx_eye_r = (right_eye_region["top_x"] + right_eye_region["bottom_x"]) / 2
        self.cy_eye_r = (right_eye_region["top_y"] + right_eye_region["bottom_y"]) / 2

        eye_width_r = (right_eye_region["bottom_x"] - right_eye_region["top_x"])
        # eye_height_r = (right_eye_region["bottom_y"] - right_eye_region["top_y"])
        
        #右目の虹彩の座標取得
        right_iris = self._detect_iris(right_eye)
        M = cv2.moments(right_iris)
        self.cx_iris_r = (M["m10"]/M["m00"]) / eye_width_r if M["m00"] != 0 else 0
        # self.cy_iris_r = (M["m01"]/M["m00"]) / eye_height_r
        self.cy_iris_r = int(M["m01"]/M["m00"]) if M["m00"] != 0 else 0
        
        #左目の座標取得
        left_eye_region = {'top_x': landmark[42][0], 'bottom_x': landmark[45][0],
            'top_y': landmark[43][1]
            if landmark[43][1] < landmark[45][1] else landmark[45][1],
            'bottom_y': landmark[47][1]
            if landmark[47][1] > landmark[46][1] else landmark[46][1]}
        left_eye = gray[left_eye_region["top_y"]:left_eye_region["bottom_y"],left_eye_region["top_x"]:left_eye_region["bottom_x"]]
        self.cx_eye_l = (left_eye_region["top_x"] + left_eye_region["bottom_x"]) / 2
        self.cy_eye_l = (left_eye_region["top_y"] + left_eye_region["bottom_y"]) / 2
        
        eye_width_l = (left_eye_region["bottom_x"] - left_eye_region["top_x"])
        # eye_height_l = (left_eye_region["bottom_y"] - left_eye_region["top_y"])
        
        #左目の虹彩の座標取得
        left_iris = self._detect_iris(left_eye)
        M = cv2.moments(left_iris)
        self.cx_iris_l = (M["m10"]/M["m00"]) / eye_width_l if M["m00"] != 0 else 0
        # self.cy_iris_l = (M["m01"]/M["m00"]) / eye_height_l
        self.cy_iris_l = int(M["m01"]/M["m00"]) if M["m00"] != 0 else 0
        
        #顔の中心(鼻)の座標取得
        self.cx_face = landmark[30][0]
        self.cy_face = landmark[30][1]
        
        self.cx_face_l = landmark[0][0]
        self.cy_face_l = landmark[0][1]
        self.cx_face_r = landmark[16][0]
        self.cy_face_r = landmark[16][1]
        self.cx_face_b = landmark[8][0]
        self.cy_face_b = landmark[8][1]

        self.right_eye_region = right_eye_region
        self.left_eye_region = left_eye_region
        self.correction_x = (self.cx_iris_r - self.cx_iris_l) / 2
        self.correction_y = (self.cy_iris_r + self.cy_iris_l) / 2
        
        self.landmark = landmark

    def output(self):
        output = []
        output.append(self.cx_iris_r)
        output.append(self.cx_iris_l)
        output.append(self.right_eye_region["top_y"])
        output.append(self.left_eye_region["top_y"])
        output.append(self.right_eye_region["bottom_y"])
        output.append(self.left_eye_region["bottom_y"])
        # output.append(self.cy_iris_r + self.right_eye_region["top_y"])
        # output.append(self.cy_iris_l + self.left_eye_region["top_y"])
        output.append(self.cy_iris_r)
        output.append(self.cy_iris_l)
        output.append(self.cx_eye_r)
        output.append(self.cy_eye_r)
        output.append(self.cx_eye_l)
        output.append(self.cy_eye_l)
        output.append(self.cx_face)
        output.append(self.cy_face)
        output.append(self.cx_face_r)
        output.append(self.cy_face_r)
        output.append(self.cx_face_l)
        output.append(self.cy_face_l)
        output.append(self.cx_face_b)
        output.append(self.cy_face_b)
        # for l in self.landmark[:48]:
        #     output.append(l[0])
        #     output.append(l[1])
        return output
    
    def get_correction(self):
        calibration = self.config_ini['Calibration']
        c1 = calibration['c1']
        c2 = calibration['c2']
        return c1, c2