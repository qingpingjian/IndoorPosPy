#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/1/18 14:46
@author: Pete
@email: yuwp_1985@163.com
@file: wifipdr.py
@software: PyCharm Community Edition
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib.ticker import  MultipleLocator, FormatStrFormatter

from comutil import *
from dataloader import loadAcceData, loadGyroData, loadMovingWifi, loadRadioMap
from ekfmodel import ExtendedKF
from fingerprint import BayesLocation
from simplepdr import PDR
from stepcounter import SimpleStepCounter


class WifiFingerprintPDR(PDR):
    def __init__(self, personID="pete"):
        PDR.__init__(self, personID)
        self.fpAlg = None
        self.fusionModel = None

    def setFusionModel(self, model):
        self.fusionModel = model

    def setWifiPosPara(self, wifiTrainList, fpAlg, moveVector, w2rRotStr):
        self.radioMap = wifiTrainList
        self.fpAlg = fpAlg
        self.moveVector = moveVector
        self.w2rRot = w2rRotStr

    def wifiPosition(self, wifiDict):
        wifiWorldLoc = self.fpAlg.bayesAlg2(wifiDict, self.radioMap)
        return wifiWorldLoc, locTransformW2R(wifiWorldLoc, self.moveVector, self.w2rRot)

    def getLocFusion(self, acceTimeList, acceValueList, gyroTimeList, gyroValueList,
                     wifiTimeList, wifiScanList):
        """
        # Count Steps and get timestamps of step start point, peak point and end point
        # For each step:
        #   (1) predict
        #   (2) observe, Here, to get wifi fingerprint position estimation
        #   (3) update for fusion
        """
        para = modelParameterDict.get(self.personID)
        # Count step
        acceValueArray = butterFilter(acceValueList)
        # Algorithm of step counter
        sc = SimpleStepCounter(para[0], para[1], para[2], para[3])
        allIndexList = sc.countStep(acceTimeList, acceValueArray)
        stIndexList = allIndexList[0::3]
        stTimeList = [acceTimeList[i] for i in stIndexList]
        peakIndexList = allIndexList[1::3]
        peakTimeList = [acceTimeList[i] for i in peakIndexList]
        edIndexList = allIndexList[2::3]
        edTimeList = [acceTimeList[i] for i in edIndexList]
        stepNum = len(stIndexList)

        # Get step length
        stepFreq = stepNum / (edTimeList[-1] - stTimeList[0])
        stepLength = para[4] * stepFreq + para[5]
        print("Step Num is %d, Step Frequency is %.3f and Step Length is %.4f" % (stepNum, stepFreq, stepLength))

        # Get rotation angle
        rotationList = rotationAngle(gyroTimeList, gyroValueList)

        # Estimate locations and forward heading
        estiLocList = [(0, 0, 0.0, 0.0)] # [(pdrx, pdry, fusionx, fusiony)]
        wifiEstList = None
        currentGyroIndex = 0
        currentWifiIndex = 0
        for i in range(len(stIndexList)):
            # Get the heading direction
            asTime = stTimeList[i]
            aeTime = edTimeList[i]
            rotStartIndex = timeAlign(asTime, gyroTimeList, currentGyroIndex)
            currentGyroIndex = rotStartIndex - 1
            rotEndIndex = timeAlign(aeTime, gyroTimeList, currentGyroIndex)
            currentGyroIndex = rotEndIndex - 1
            direction = meanAngle(rotationList[rotStartIndex:rotEndIndex + 1])
            # TODO: Don't need to update step length?

            # update the location
            lastLoc = estiLocList[-1]
            xLoc = lastLoc[0] + stepLength * math.sin(direction)
            yLoc = lastLoc[1] + stepLength * math.cos(direction)
            if self.fusionModel == None:
                estiLocList.append((xLoc, yLoc, xLoc, yLoc))
                continue

            # Predict
            self.fusionModel.predict(stepLength, direction)
            pdrEstLoc = self.fusionModel.getEstLocation()
            # Observe
            wifiReltiveLoc = pdrEstLoc
            if self.fpAlg != None:
                # From the current peak timestamp to next peak timestamp
                startWifiTime = peakTimeList[i]
                endWifiTime = peakTimeList[i + 1] if i < len(stIndexList) - 1 else wifiTimeList[-1]
                currentWifiIndex, currentWifiDict = wifiExtract(startWifiTime, endWifiTime, wifiTimeList, wifiScanList, currentWifiIndex)
                if currentWifiDict != None:
                    wifiWorldLoc, wifiReltiveLoc = self.wifiPosition(currentWifiDict)
                    if wifiEstList == None:
                        wifiEstList = [(i, wifiWorldLoc[0], wifiWorldLoc[1])]
                    else:
                        wifiEstList.append((i, wifiWorldLoc[0], wifiWorldLoc[1]))
            # Fusion
            self.fusionModel.update(np.matrix([ [wifiReltiveLoc[0]], [wifiReltiveLoc[1]] ]))
            fusionLocx, fusionLocy = self.fusionModel.getEstLocation()
            estiLocList.append((xLoc, yLoc, fusionLocx, fusionLocy))
        return estiLocList, wifiEstList


if __name__ == "__main__":
    sensorFilePath = ("./Examples/ExtendedKF/20180118102918_acce.csv",
                      "./Examples/ExtendedKF/20180118102918_gyro.csv",
                      "./Examples/ExtendedKF/20180118102918_wifi.csv" )
    trainFileDir = "./RawData/RadioMap"

    locationFilePath = "./Examples/ExtendedKF/20180118102918_route.csv"
    #pdrEstimateFilePath = "./Examples/ExtendedKF/20180118102918_estimate_pdr.csv"
    ekfEstimateFilePath = "./Examples/ExtendedKF/20180118102918_estimate_ekf.csv"
    wifiEstimateFilePath = "./Examples/ExtendedKF/20180118102918_estimate_wifi.csv"
    # From local coordinate to global coordiante, they are related to route starting point and direction
    r2wRotStr = "270"
    w2rRotStr = "90"
    moveVector = (39.3,10.4)
    # {14, 1, 15} 14 step straight forward, then 1 step turn left, last 15 steps straight forward
    stepTruth = 30

    # Load sensor data and moving wifi scan from files
    acceTimeList, acceValueList = loadAcceData(sensorFilePath[0], relativeTime=False)
    gyroTimeList, gyroValueList = loadGyroData(sensorFilePath[1], relativeTime=False)
    wifiTimeList, wifiScanList = loadMovingWifi(sensorFilePath[2])
    # Load wifi radio map
    # load radio map will time cost process, so we print some messages
    print("Start loading radio map ...")
    wifiTrainDict = loadRadioMap(trainFileDir, statFlag=True)
    trainLocList = []
    trainWifiList = []
    for userID in wifiTrainDict.keys():
        trainLocList.extend(wifiTrainDict.get(userID)[0])
        # 1: wifiDict, 2: wifiGaussianParaDict, so we use 2 here.
        trainWifiList.extend(wifiTrainDict.get(userID)[2])
    wifiTrainList = [trainLocList, trainWifiList]
    print("Complete loading radio map.")

    # Get the simple PDR estimations and related wifi estimations, then get the fusion based EFK
    # (1) Define a extended kalman filter model
    initState = np.matrix([[0.0], [0.0], [0.0]])
    processCov = np.diag([0.098, 0.81, 0.81])
    observeTrans = np.matrix([[0, 1, 0], [0, 0, 1]])
    observeCov = np.diag([100.0, 100.0])
    firstEKF = ExtendedKF(initState, processCov, observeTrans, observeCov)

    fusionPdr = WifiFingerprintPDR()
    fusionPdr.setFusionModel(firstEKF)
    fusionPdr.setWifiPosPara(wifiTrainList, BayesLocation(apNum=15), moveVector, w2rRotStr)
    locEstRelList, wifiEstWorldList = fusionPdr.getLocFusion(acceTimeList, acceValueList, gyroTimeList, gyroValueList,
                                          wifiTimeList, wifiScanList)
    locEstWorldLoc = []
    for relLoc in locEstRelList:
        pdrWorldLoc = locTransformR2W((relLoc[0], relLoc[1]), moveVector, r2wRotStr)
        fusionWorldLoc = locTransformR2W((relLoc[2], relLoc[3]), moveVector, r2wRotStr)
        locEstWorldLoc.append((pdrWorldLoc[0], pdrWorldLoc[1], fusionWorldLoc[0], fusionWorldLoc[1]))

    # Save the estimate locations
    locEstList = [(round(loc[0] * 1000) / 1000, round(loc[1] * 1000) / 1000,
                   round(loc[2] * 1000) / 1000, round(loc[3] * 1000) / 1000) for loc in locEstWorldLoc]
    locEstDF = pd.DataFrame(np.array(locEstList), columns=["EX(m)", "EY(m)", "OX(m)", "OY(m)"])
    locEstDF.to_csv(ekfEstimateFilePath, encoding='utf-8', index=False)

    wifiEstList = [(int(loc[0]), round(loc[1] * 1000) / 1000, round(loc[2] * 1000) / 1000) for loc in wifiEstWorldList]
    wifiEstDF = pd.DataFrame(np.array(wifiEstList), columns=["SI", "EX(m)", "EY(m)"])
    wifiEstDF.to_csv(wifiEstimateFilePath, encoding='utf-8', index=False)

    # load real locations
    locRealDF = pd.read_csv(locationFilePath)

    # Calculate the location errors
    locRealList = [(loc[0], loc[1]) for loc in locRealDF.values]
    locPDRList = [(loc[0], loc[1]) for loc in locEstList]
    locFusionList = [(loc[2], loc[3]) for loc in locEstList]
    pdrErrList = distError(locRealList, locPDRList)
    fusionErrList = distError(locRealList, locFusionList)
    # Wifi errors
    wifiErrList = []
    for wifiEst in wifiEstList:
        si = wifiEst[0] if wifiEst[0] < len(locRealList) else len(locRealList) - 1
        realLoc = locRealList[si]
        errorDist = math.sqrt((realLoc[0] - wifiEst[1])**2 + (realLoc[1] - wifiEst[2])**2)
        wifiErrList.append((si, errorDist))

    # Save the errors
    fusionErrList = [round(err * 1000) / 1000 for err in fusionErrList]
    errorFilePath = "%s_error.csv" % locationFilePath[0:-4]
    errorDF = pd.DataFrame(np.array(fusionErrList), columns=["Error(m)"])
    errorDF.to_csv(errorFilePath, encoding='utf-8', index=False)

    print("Average Error Distance is %.3f" % np.mean(fusionErrList))

    # Show the errors
    pdrxMajorLocator = MultipleLocator(10)
    pdrxMajorFormatter = FormatStrFormatter("%d")
    pdrxMinorLocator = MultipleLocator(5)
    pdryMajorLocator = MultipleLocator(1.0)
    pdryMajorFormatter = FormatStrFormatter("%.1f")
    pdryMinorLocator = MultipleLocator(0.5)

    fig = plt.figure()
    pdrAxe = fig.add_subplot(111)

    pdrAxe.xaxis.set_major_locator(pdrxMajorLocator)
    pdrAxe.xaxis.set_major_formatter(pdrxMajorFormatter)
    pdrAxe.xaxis.set_minor_locator(pdrxMinorLocator)
    pdrAxe.yaxis.set_major_locator(pdryMajorLocator)
    pdrAxe.yaxis.set_major_formatter(pdryMajorFormatter)
    pdrAxe.yaxis.set_minor_locator(pdryMinorLocator)
    pdrAxe.set_xlabel("$Step\ Number$")
    pdrAxe.set_ylabel("$Position\ Error(m)$")
    pdrAxe.plot(range(len(fusionErrList)), fusionErrList, color="r", lw=2, label="PDR Combined Wi-Fi")
    pdrAxe.plot(range(len(pdrErrList)), pdrErrList, color="b", lw=2, label="Basic PDR")
    pdrAxe.plot([wifiError[0] for wifiError in wifiErrList], [wifiError[1] for wifiError in wifiErrList],
                color="y", marker="x", lw=2, label="Wi-Fi")
    plt.legend(loc="best")
    plt.grid()
    plt.show()

    print("Done.")