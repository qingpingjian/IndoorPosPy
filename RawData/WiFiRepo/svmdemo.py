#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/4/20 20:56
@author: Pete
@email: yuwp_1985@163.com
@file: svmdemo.py
@software: PyCharm Community Edition
"""
import math
import numpy as np
import pandas as pd
import timeit

from sklearn import svm

def accuracy(predictions, labels):
    squareSum = np.sum((predictions-labels)**2, 1)
    print(type(squareSum))
    print(squareSum.shape)
    print(squareSum)
    c = np.array([v for v in squareSum])
    print(c.shape, type(c))
    print(np.sqrt(c))    
    np.sqrt(np.array([v for v in squareSum]))
    acc = np.mean([math.sqrt(v) for v in squareSum])
    return acc

def firstSVM(wfTrain, posTrain, wfTest, posTest, logFlag=False):
    if logFlag:
        print("Start to fit SVR model ...")
    clfPosX = svm.SVR(gamma=0.01)
    clfPosY = svm.SVR(gamma=0.01)
    clfPosX.fit(wfTrain, posTrain[:,0])
    clfPosY.fit(wfTrain, posTrain[:,1])

    if logFlag:
        print("Start to predict the position by SVR ...")
    xPred = clfPosX.predict(wfTest)
    yPred = clfPosY.predict(wfTest)

    posPred = np.column_stack((xPred, yPred))
    acc = accuracy(posPred, posTest)
    print("The mean positioning error is: %.3f" % (acc))
    return

if __name__ == "__main__":
    trainWifiFilePath = "20180420-wifi_train.csv"
    testWifiFilePath = "20180420-wifi_test.csv"
    
    # Get train Wi-Fi fingerprints data set    
    trainWifiDF = pd.read_csv(trainWifiFilePath)
    trainWifiInfo = trainWifiDF.values
    colsN = trainWifiInfo.shape[1]
    wifiTrain = trainWifiInfo[:,0:-3]
    posTrain = trainWifiInfo[:, colsN-3:-1]
    
    # Get test Wi-Fi fingerprints data set
    testWifiDF = pd.read_csv(testWifiFilePath)
    testWifiInfo = testWifiDF.values
    colsN = testWifiInfo.shape[1]
    wifiTest = testWifiInfo[:,0:-3]
    posTest = testWifiInfo[:,colsN-3:-1]

    # Support Vector Machine for Regression
    firstSVM(wifiTrain, posTrain, wifiTest, posTest, logFlag=True)
 
    print("Done.")
