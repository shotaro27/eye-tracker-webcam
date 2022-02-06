# -*- coding: utf-8 -*-
"""
@author: shotaro27
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt

dir_path = os.path.dirname(__file__)

output_path = os.path.join(dir_path,"outputs\\output.csv")
with open(output_path) as f:
    reader = csv.reader(f)
    global x1, x2, y1, y2
    x1 = []
    x2 = []
    y1 = []
    y2 = []
    rows = [row for row in reader]
    for row in rows:
        # x1.append([float(x_d1) for x_d1 in np.array(row)[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13]]])
        # x2.append([float(x_d2) for x_d2 in np.array(row)[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13]]])
        x1.append([float(x_d1) for x_d1 in row[:-2]])
        x2.append([float(x_d2) for x_d2 in row[:-2]])
        y1.append(int(row[-2]))
        y2.append(int(row[-1]))

test_output_path = os.path.join(dir_path,"outputs\\test_output.csv")
with open(test_output_path) as f:
    reader = csv.reader(f)
    global testx1, testx2, testy1, testy2
    testx1 = []
    testx2 = []
    testy1 = []
    testy2 = []
    rows = [row for row in reader]
    for row in rows:
        testx1.append([float(x_d1) for x_d1 in row[:-2]])
        testx2.append([float(x_d2) for x_d2 in row[:-2]])
        testy1.append(int(row[-2]))
        testy2.append(int(row[-1]))

#x座標(y1)の機械学習
from sklearn.linear_model import LinearRegression
average_x = []
average_y = []
photocount = []
for t, x in enumerate(x1):
    if t<=300: continue
    model1 = LinearRegression()
    model1.fit(x1[:t], y1[:t]) 

    #y座標(y2)の機械学習
    model2 = LinearRegression()
    model2.fit(x2[:t], y2[:t])

    accuracy_x = []
    accuracy_y = []

    test_x = testx1
    test_y = testx2
    correct_x = testy1
    correct_y = testy2
    for i, x_list in enumerate(test_x):
        y_pred_y1 = model1.predict([test_x[i]])#座標
        y_pred_y2 = model2.predict([test_y[i]])
        
        result_x = y_pred_y1[0]
        result_y = y_pred_y2[0]
        
        accuracy_x.append(abs(result_x - correct_x[i]))
        accuracy_y.append(abs(result_y - correct_y[i]))
        
    # print(model1.coef_)
    # print(model1.intercept_)
    # print(model2.coef_)
    # print(model2.intercept_)
    photocount.append(t)
    average_x.append(np.average(accuracy_x))
    average_y.append(np.average(accuracy_y))
    print(np.average(accuracy_x))
    print(np.average(accuracy_y))

print(testy1)

plt.plot(photocount, average_x)
plt.show()

plt.plot(photocount, average_y)
plt.show()