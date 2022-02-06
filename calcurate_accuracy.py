# -*- coding: utf-8 -*-
"""
@author: shotaro27
"""

import os
import csv
import pickle
import numpy as np

dir_path = os.path.dirname(__file__)

output_path = os.path.join(dir_path,"outputs\\test_output.csv")
with open(output_path) as f:
    reader = csv.reader(f)
    global X, y1, y2
    X = []
    y1 = []
    y2 = []
    # rows = [row for row in reader]
    # t = int(len(rows) / 10 * 7)
    # test_rows = rows[t:]
    test_rows = [row for row in reader]
    for row in test_rows:
        X.append([float(datas) for datas in row[0:-2]])
        y1.append(int(row[-2]))
        y2.append(int(row[-1]))

print(y1)

model1_path = os.path.join(dir_path,"model\\model1.pickle")
model2_path = os.path.join(dir_path,"model\\model2.pickle")

with open(model1_path, mode='rb') as f:
    model1 = pickle.load(f)

with open(model2_path, mode='rb') as f:
    model2 = pickle.load(f)

accuracy_x = []
accuracy_y = []

for i, x_list in enumerate(X):
    y_pred_y1 = model1.predict([x_list])#座標
    y_pred_y2 = model2.predict([x_list])
    
    result_x = y_pred_y1[0]
    result_y = y_pred_y2[0]
    
    #accuracy_x.append(100 - abs(100 - abs(result_x / y1[i]) * 100))
    #accuracy_y.append(100 - abs(100 - abs(result_y / y2[i]) * 100))
    
    accuracy_x.append(abs(result_x - y1[i]))
    accuracy_y.append(abs(result_y - y2[i]))

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
print(model1.coef_)
print(model1.intercept_)
print(model2.coef_)
print(model2.intercept_)
print(np.average(accuracy_x))
print(np.average(accuracy_y))
    