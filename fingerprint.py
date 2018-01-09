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

from cdfdemo import cdf
from dataloader import loadRadioMap, loadWifiTest
from wififunc import eulerDistanceA

class KNNLocation(object):
    def __init__(self, nNeighbours=5, apNum=7, wifiDefault=-100.0):
        self.nNeighbours = nNeighbours
        self.apNum = apNum
        self.wifiDefault = wifiDefault

    def weightedMean(self, eulerDistList):
        eulerWeightList = [eulerDist[1] for eulerDist in eulerDistList]
        weightSum = np.sum(eulerWeightList)
        eulerWeightList = [ew / weightSum for ew in eulerWeightList]
        xWeight = 0.0
        yWeight = 0.0
        for i in range(len(eulerDistList)):
            xWeight += eulerDistList[i][0][0] * eulerWeightList[i]
            yWeight += eulerDistList[i][0][1] * eulerWeightList[i]
        return (xWeight, yWeight)

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
                # []
                eulerDistList.append((wifiTrainList[0][j], eulerDistanceA(wifiTestList[1][i], wifiTrainList[1][j], self.apNum, self.wifiDefault)))
            topKDistList = sorted(eulerDistList, key=lambda x: x[1])[0:self.nNeighbours]
            estLoc = self.weightedMean([(eulerDist[0], 1.0 / eulerDist[1]) for eulerDist in topKDistList])
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


class BayesLocation(KNNLocation):
    def __init__(self, nNeighbours=5, apNum=7, wifiDefault=-100.0):
        KNNLocation.__init__(self, nNeighbours, apNum, wifiDefault)

    def bayesAlg(self, wifiTestList, wifiTrainList):
        pass


if __name__ == "__main__":
    trainFileDir = "./RawData/RadioMap"
    testFileDir = "./RawData/WifiTest"
    estimationKNNFilePath = "./Examples/Fingerprint/20180104205655_estimate_knn.csv"
    wifiTrainDict = loadRadioMap(trainFileDir)
    wifiTestDict = loadWifiTest(testFileDir)

    firstKNN = KNNLocation(apNum=7)
    knnEstimateList = firstKNN.estimation(wifiTestDict, wifiTrainDict, multiDevice=False)

    # Save knn estimate results
    locEstDF = pd.DataFrame(np.array(knnEstimateList), columns=["X(m)", "Y(m)", "EX(m)", "EY(m)"])
    locEstDF.to_csv(estimationKNNFilePath, encoding='utf-8', index=False)

    # Show error CDF
    errorList = []
    for locates in knnEstimateList:
        errorList.append(round(math.sqrt((locates[0] - locates[2])**2 + (locates[1] - locates[3])**2) * 1000) / 1000)

    print(sorted(errorList))
    X, Y = cdf(errorList, False)

    fig = plt.figure()
    knnAxe = fig.add_subplot(111)
    knnAxe.set_xlabel("$Position\ Error(m)$")
    knnAxe.set_ylabel("$Probability$")
    knnAxe.plot(X, Y, label="kNN")

    plt.legend(loc = 2)
    plt.grid()
    plt.show()

    print("Done.")