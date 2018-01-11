#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/1/9 9:23
@author: Pete
@email: yuwp_1985@163.com
@file: fingerprint.py
@software: PyCharm Community Edition
"""

import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from comutil import cdf, meanLocation
from dataloader import loadRadioMap, loadWifiTest
from wififunc import eulerDistanceA, bayesProbability

class KNNLocation(object):
    def __init__(self, nNeighbours=5, apNum=7, wifiDefault=-100.0):
        self.nNeighbours = nNeighbours
        self.apNum = apNum
        self.wifiDefault = wifiDefault

    def knnAlg(self, wifiTestList, wifiTrainList):
        """
        :param wifiTestList: [ [loc1, loc2, loc3], [wifiDict1, wifiDict2, wifiDict3]]
        :param wifiTrainList: the same as above
        :return: [(loc1, estLoc1), (loc2, estLoc2), (loc3, estLoc3)]
        """
        estimateList = []
        for i in range(len(wifiTestList[0])):
            eulerDistList = []
            for j in range(len(wifiTrainList[0])):
                eulerDistList.append((wifiTrainList[0][j], eulerDistanceA(wifiTestList[1][i], wifiTrainList[1][j], self.apNum, self.wifiDefault)))
            topKDistList = sorted(eulerDistList, key=lambda x: x[1])[0:self.nNeighbours]
            estLoc = meanLocation([(eulerDist[0], 1.0 / eulerDist[1]) for eulerDist in topKDistList])
            estimateList.append((wifiTestList[0][i][0], wifiTestList[0][i][1], estLoc[0], estLoc[1]))
        return estimateList

    def estimation(self, wifiTestDict, wifiTrainDict, multiDevice=False):
        wifiTestList = []
        wifiTrainList = []
        estimateList = []
        if multiDevice:
            testLocList = []
            testWifiList = []
            for userID in wifiTestDict.keys():
                testLocList.extend(wifiTestDict.get(userID)[0])
                testWifiList.extend(wifiTestDict.get(userID)[1])
            wifiTestList.append(testLocList)
            wifiTestList.append(testWifiList)
            trainLocList = []
            trainWifiList = []
            for userID in wifiTrainDict.keys():
                trainLocList.extend(wifiTrainDict.get(userID)[0])
                trainWifiList.extend(wifiTrainDict.get(userID)[1])
            wifiTrainList.append(trainLocList)
            wifiTrainList.append(trainWifiList)
            estimateList = self.knnAlg(wifiTestList, wifiTrainList)
        else:
            for userID in wifiTestDict.keys():
                wifiTestList = wifiTestDict.get(userID)
                wifiTrainList = wifiTrainDict.get(userID)
                estimateList.extend(self.knnAlg(wifiTestList, wifiTrainList))
        return estimateList


class BayesLocation(object):
    def __init__(self, nNeighbours=5, apNum=7, wifiDefault=-100.0):
        self.nNeighbours = nNeighbours
        self.apNum = apNum
        self.wifiDefault = wifiDefault

    def bayesAlg(self, wifiTestList, wifiTrainList):
        """
        :param wifiTestList: [ [loc1, loc2, loc3], [wifiDict1, wifiDict2, wifiDict3]]
        :param wifiTrainList: [ [loc1, loc2, loc3], [wifiGDP1, wifiGDP2, wifiGDP3]]
        :return: [(loc1, estLoc1), (loc2, estLoc2), (loc3, estLoc3)]
        """
        estimateList = []
        for i in range(len(wifiTestList[0])):
            bayesProbList = []
            for j in range(len(wifiTrainList[0])):
                bayesProbList.append((wifiTrainList[0][j], bayesProbability(wifiTestList[1][i], wifiTrainList[1][j], self.apNum, self.wifiDefault)))
            estLoc = meanLocation(sorted(bayesProbList, key=lambda x: x[1], reverse=True)[0:self.nNeighbours], weightedMean=False)
            estimateList.append((wifiTestList[0][i][0], wifiTestList[0][i][1], estLoc[0], estLoc[1]))
        return estimateList

    def estimation(self, wifiTestDict, wifiTrainDict, multiDevice=False):
        wifiTestList = []
        wifiTrainList = []
        estimateList = []
        if multiDevice:
            testLocList = []
            testWifiList = []
            for userID in wifiTestDict.keys():
                testLocList.extend(wifiTestDict.get(userID)[0])
                testWifiList.extend(wifiTestDict.get(userID)[1])
            wifiTestList.append(testLocList)
            wifiTestList.append(testWifiList)
            trainLocList = []
            trainWifiList = []
            for userID in wifiTrainDict.keys():
                trainLocList.extend(wifiTrainDict.get(userID)[0])
                # 1: wifiDict, 2: wifiGaussianParaDict, so we use 2 here.
                trainWifiList.extend(wifiTrainDict.get(userID)[2])
            wifiTrainList.append(trainLocList)
            wifiTrainList.append(trainWifiList)
            estimateList = self.bayesAlg(wifiTestList, wifiTrainList)
        else:
            for userID in wifiTestDict.keys():
                wifiTestList = wifiTestDict.get(userID)
                wifiTrainList = wifiTrainDict.get(userID)[0::2]
                estimateList.extend(self.bayesAlg(wifiTestList, wifiTrainList))
        return estimateList


if __name__ == "__main__":
    trainFileDir = "./RawData/RadioMap"
    testFileDir = "./RawData/WifiTest"
    estimationKNNFilePath = "./Examples/Fingerprint/20180104205655_estimate_knn.csv"
    estimationBayesFilePath = "./Examples/Fingerprint/20180104205655_estimate_bayes.csv"

    # load test and train data
    wifiTrainDict = loadRadioMap(trainFileDir, statFlag=True)
    wifiTestDict = loadWifiTest(testFileDir)

    # KNN location algorithm
    firstKNN = KNNLocation(apNum=15)
    knnEstimateList = firstKNN.estimation(wifiTestDict, wifiTrainDict, multiDevice=False)

    # Save knn estimate results
    knnEstDF = pd.DataFrame(np.array(knnEstimateList), columns=["X(m)", "Y(m)", "EX(m)", "EY(m)"])
    knnEstDF.to_csv(estimationKNNFilePath, encoding='utf-8', index=False)

    knnErrorList = [round(math.sqrt((locates[0] - locates[2]) ** 2 + (locates[1] - locates[3]) ** 2) * 1000) / 1000
                    for locates in knnEstimateList]

    # print(sorted(knnErrorList))
    X1, Y1 = cdf(knnErrorList)
    print("The mean location error is %.3f" % np.mean(knnErrorList))

    # Native Bayes location algorithm
    firstBayes = BayesLocation(apNum=15)
    bayesEstimateList = firstBayes.estimation(wifiTestDict, wifiTrainDict, multiDevice=False)

    # Save native bayes estimate results
    bayesEstDF = pd.DataFrame(np.array(bayesEstimateList), columns=["X(m)", "Y(m)", "EX(m)", "EY(m)"])
    bayesEstDF.to_csv(estimationBayesFilePath, encoding='utf-8', index=False)

    bayesErrorList = [round(math.sqrt((locates[0] - locates[2]) ** 2 + (locates[1] - locates[3]) ** 2) * 1000) / 1000
                      for locates in bayesEstimateList]

    print(sorted(bayesErrorList))
    X2, Y2 = cdf(bayesErrorList)
    print("The mean location error is %.3f" % np.mean(bayesErrorList))

    # Show error CDF
    fig = plt.figure()
    knnAxe = fig.add_subplot(111)
    knnAxe.set_xlabel("$Position\ Error(m)$")
    knnAxe.set_ylabel("$Cumulative\ Probability$")
    knnAxe.plot(X1, Y1, color="r", label="kNN")
    knnAxe.plot(X2, Y2, color="b", label="Native Bayes")

    plt.legend(loc = 2)
    plt.grid()
    plt.show()

    print("Done.")