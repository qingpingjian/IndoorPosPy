#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/4/21 上午1:46
@author: Pete
@email: yuwp_1985@163.com
@file: mlpdemo.py
@software: PyCharm Community Edition
"""
import numpy as np
import pandas as pd

from sklearn.neural_network import  MLPRegressor

def accuracy(predictions, labels):
    squareSum = np.sum((predictions-labels)**2, 1)
    return np.mean(np.sqrt(squareSum.astype(np.float32)))

def firstMLP(wfTrain, posTrain, wfTest, posTest):
    clf = MLPRegressor(hidden_layer_sizes=(500, 250))
    clf.fit(wfTrain, posTrain)
    posPred = clf.predict(wfTest)
    acc = accuracy(posPred, posTest)
    print ("Accuracy is: %.3f" % (acc))

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

    firstMLP(wifiTrain, posTrain, wifiTest, posTest)

    print("Done.")
