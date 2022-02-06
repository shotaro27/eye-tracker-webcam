# -*- coding: utf-8 -*-
"""
@author: shotaro27
"""

import os
import csv
import pickle

dir_path = os.path.dirname(__file__)

output_path = os.path.join(dir_path,"outputs\\output.csv")
with open(output_path) as f:
    reader = csv.reader(f)
    global X, y1, y2
    X = []
    y1 = []
    y2 = []
    # rows = [row for row in reader]
    # t = int(len(rows) / 10 * 7)
    # data_rows = rows[:t]
    data_rows = [row for row in reader]
    for row in data_rows:
        X.append([float(datas) for datas in row[0:-2]])
        y1.append(int(row[-2]))
        y2.append(int(row[-1]))

print(y1)

#x座標(y1)の機械学習
from sklearn.linear_model import LinearRegression
model1 = LinearRegression()
model1.fit(X, y1) 

#y座標(y2)の機械学習
model2 = LinearRegression()
model2.fit(X, y2) 

model1_path = os.path.join(dir_path,"model\\model1.pickle")
model2_path = os.path.join(dir_path,"model\\model2.pickle")

with open(model1_path, mode='wb') as f:
    pickle.dump(model1, f, protocol=2)

with open(model2_path, mode='wb') as f:
    pickle.dump(model2, f, protocol=2)