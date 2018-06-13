#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/6/13 9:25
@author: Pete
@email: yuwp_1985@163.com
@file: knnroom.py
@software: PyCharm Community Edition
"""
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn import neighbors
from dataloader2 import load_wifi_data


def get_accuracy(test_label_list, test_predict_list):
    sample_num = min(len(test_label_list), len(test_predict_list))
    correct_num = np.sum([test_label_list[i] == test_predict_list[i] for i in range(sample_num)])
    return float(correct_num) * 1.0 / sample_num


def first_knn_classifier(train_file, test_file, default_wifi, k):
    wifi_train_dict = load_wifi_data(train_file)
    wifi_test_dict = load_wifi_data(test_file)
    build_list = wifi_test_dict.keys()
    test_label_list = []
    test_predict_list = []
    for build_id in build_list:
        wifi_test_info = wifi_test_dict.get(build_id)
        wifi_test_X = np.array(wifi_test_info[0])
        wifi_test_X[wifi_test_X > 0] = default_wifi
        wifi_test_y = np.array(wifi_test_info[1]).astype(int) / 1000 # TODO: 需要注意的是测试数据集中不包括SPACEID的信息
        wifi_train_info = wifi_train_dict.get(build_id)
        wifi_train_X = np.array(wifi_train_info[0])
        wifi_train_X[wifi_train_X > 0] = default_wifi
        wifi_train_y = np.array(wifi_train_info[1]).astype(int) / 1000

        label_encoder = LabelEncoder()
        wifi_all_room_List = np.concatenate((wifi_train_y, wifi_test_y))
        label_encoder.fit(wifi_all_room_List)
        wifi_train_label = label_encoder.transform(wifi_train_y)
        wifi_test_label = label_encoder.transform(wifi_test_y)

        knn_room_cls = neighbors.KNeighborsClassifier(n_neighbors=k)
        knn_room_cls.fit(wifi_train_X, wifi_train_label)
        wifi_test_predict = knn_room_cls.predict(wifi_test_X)
        test_label_list.extend(wifi_test_label)
        test_predict_list.extend(wifi_test_predict)
    return get_accuracy(test_label_list, test_predict_list)


if __name__ == "__main__":
    wifi_train_file = "trainingData.csv"
    wifi_validate_file = "validationData.csv"
    default_wifi_list = range(-90, -106, -1)
    k_para_list = range(1, 22, 2)
    for default_value in default_wifi_list:
        for k_para in k_para_list:
            accuracy = first_knn_classifier(wifi_train_file, wifi_validate_file, default_value, k_para)
            print ("Default Wi-Fi: %f, Top K: %d, Accuracy: %.3f%%" % (default_value, k_para, accuracy * 100))

    print("Done.")