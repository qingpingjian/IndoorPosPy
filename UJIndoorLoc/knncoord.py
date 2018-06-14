#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/6/13 22:36
@author: Pete
@email: yuwp_1985@163.com
@file: knncoord.py
@software: PyCharm Community Edition
"""
import numpy as np
from sklearn import neighbors
from dataloader2 import load_wifi_data

def accuracy(predictions, labels):
    squareSum = np.sum(np.array((predictions-labels))**2, axis=1)
    return np.mean(np.sqrt(squareSum.astype(np.float32)))

def first_knn_regress(train_file, test_file, default_wifi, k):
    wifi_train_dict = load_wifi_data(train_file)
    wifi_test_dict = load_wifi_data(test_file)
    build_list = wifi_test_dict.keys()

    test_label_list = None
    test_predict_list = None
    for build_id in build_list:
        wifi_test_info = wifi_test_dict.get(build_id)
        wifi_test_X = np.array(wifi_test_info[0])
        wifi_test_X[wifi_test_X > 0] = default_wifi
        wifi_test_y = np.array(wifi_test_info[2])
        wifi_train_info = wifi_train_dict.get(build_id)
        wifi_train_X = np.array(wifi_train_info[0])
        wifi_train_X[wifi_train_X > 0] = default_wifi
        wifi_train_y = np.array(wifi_train_info[2])

        knn_regress = neighbors.KNeighborsRegressor(n_neighbors=k, weights="distance", metric="euclidean")
        knn_regress.fit(wifi_train_X, wifi_train_y)
        wifi_test_predict = knn_regress.predict(wifi_test_X)

        if test_label_list is None:
            test_label_list = wifi_test_y
        else:
            test_label_list = np.concatenate((test_label_list, wifi_test_y), axis=0)
        if test_predict_list is None:
            test_predict_list = wifi_test_predict
        else:
            test_predict_list = np.concatenate((test_predict_list, wifi_test_predict), axis=0)
    return accuracy(test_label_list, test_predict_list)

if __name__ == "__main__":
    wifi_train_file = "trainingData.csv"
    wifi_validate_file = "validationData.csv"
    default_wifi_list = range(-90, -106, -1)
    k_para_list = range(1, 32, 2)
    # default_wifi_list = [-92]
    # k_para_list = [5]
    for default_value in default_wifi_list:
        for k_para in k_para_list:
            meanPosErr = first_knn_regress(wifi_train_file, wifi_validate_file, default_value, k=k_para)
            print ("Default Wi-Fi: %f, Top K: %d, Mean Error: %.3f" % (default_value, k_para, float(meanPosErr)))

    print("Done.")