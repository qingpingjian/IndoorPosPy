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


def first_knn_regress():
    pass

if __name__ == "__main__":
    wifi_train_file = "trainingData.csv"
    wifi_validate_file = "validationData.csv"
    default_wifi_list = range(-90, -106, -1)
    k_para_list = range(1, 22, 2)
    default_wifi_list = [-92]
    k_para_list = [5]
    first_knn_regress()
    print("Done.")