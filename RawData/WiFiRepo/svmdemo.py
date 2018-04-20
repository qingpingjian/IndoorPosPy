#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/4/20 20:56
@author: Pete
@email: yuwp_1985@163.com
@file: svmdemo.py
@software: PyCharm Community Edition
"""
import numpy as np
import pandas as pd

from sklearn import svm

def accuracy(predictions, labels):
    return np.mean(np.sqrt(np.sum((predictions - labels)**2, 1)))

def firstSVM():
    pass

if __name__ == "__main__":
    testWifiFilePath = "20180420-wifi_test.csv"
    trainWifiFilePath = "20180420-wifi_train.csv"

    testWifiDF = pd.read_csv(testWifiFilePath)
    Xtest = testWifiDF.ix[:,0:-3]



    print("Done.")