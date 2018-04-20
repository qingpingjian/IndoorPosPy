#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/4/21 上午12:25
@author: Pete
@email: yuwp_1985@163.com
@file: knndemo.py
@software: PyCharm Community Edition
"""
import numpy as np
import pandas as pd

from sklearn import neighbors

def accuracy(predictions, labels):
    squareSum = np.sum((predictions-labels)**2, 1)
    return np.mean(np.sqrt(squareSum.astype(np.float32)))

def firstKNN(wifiTrain, posTrain, wifiTest, posTest):
    knnPos = neighbors.KNeighborsRegressor(metric="euclidean")
    knnPos.fit(wifiTrain, posTrain)
    posPred = knnPos.predict(wifiTest)
    print ("Accuracy is: %.3f" % (accuracy(posPred, posTest)))


if __name__ == "__main__":
    trainWifiFilePath = "20180420-wifi_train.csv"
    testWifiFilePath = "20180420-wifi_test.csv"

    # Get train Wi-Fi fingerprints data set
    trainWifiDF = pd.read_csv(trainWifiFilePath)
    trainWifiInfo = trainWifiDF.values
    colsN = trainWifiInfo.shape[1]
    wifiTrain = trainWifiInfo[:, 0:-3]
    posTrain = trainWifiInfo[:, colsN - 3:-1]

    # Get test Wi-Fi fingerprints data set
    testWifiDF = pd.read_csv(testWifiFilePath)
    testWifiInfo = testWifiDF.values
    colsN = testWifiInfo.shape[1]
    wifiTest = testWifiInfo[:, 0:-3]
    posTest = testWifiInfo[:, colsN - 3:-1]

    firstKNN(wifiTrain, posTrain, wifiTest, posTest)

    print("Done.")
