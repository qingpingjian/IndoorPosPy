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
import timeit

from sklearn import svm

def accuracy(predictions, labels):
    return np.mean(np.sqrt(np.sum((predictions - labels)**2, 1)))

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
    colsN = trainWifiDF.values.shape[1]
    wifiTrain = trainWifiDF.ix[:,0:-3]
    posTrain = trainWifiDF.ix[:, colsN-3:]

    # Get test Wi-Fi fingerprints data set
    testWifiDF = pd.read_csv(testWifiFilePath)
    colsN = testWifiDF.values.shape[1]
    wifiTest = testWifiDF.ix[:,0:-3]
    posTest = testWifiDF.ix[:,colsN-3:]

    # Support Vector Machine for Regression
    firstSVM(wifiTrain, posTrain, wifiTest, posTest, logFlag=True)
 
    print("Done.")
