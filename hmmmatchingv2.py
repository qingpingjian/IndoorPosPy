#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/5/15 22:22
@author: Pete
@email: yuwp_1985@163.com
@file: hmmmatchingv2.py.py
@software: PyCharm Community Edition
"""
import pandas as pd
import time

from comutil import *
from abstractmap import *
from dataloader import loadAcceData, loadGyroData, loadMovingWifi
from stepcounter import SimpleStepCounter

class AiFiMatcher(object):
    def __init__(self, personID="pete"):
        self.personID = personID
        return

    def updateDigitalMap(self, indoorMap):
        self.digitalMap = indoorMap

    def updateRadioMap(self, radioMap):
        self.radioMap = radioMap

    def onlineViterbi(self, acceTimeList, acceValueList,
                      gyroTimeList, gyroValueList,
                      wifiTimeList=None, wifiScanList=None,
                      startingDirection=0.0,
                      stepError=0, headingError=0):
        para = modelParameterDict.get(self.personID)
        # Count step
        acceValueArray = butterFilter(acceValueList)
        # Algorithm of step counter
        sc = SimpleStepCounter(self.personID)
        allIndexList = sc.countStep(acceTimeList, acceValueArray)
        stIndexList = allIndexList[0::3]
        stTimeList = [acceTimeList[i] for i in stIndexList]
        edIndexList = allIndexList[2::3]
        edTimeList = [acceTimeList[i] for i in edIndexList]
        stepNum = len(stIndexList)

        # Get step length
        stepFreq = stepNum / (edTimeList[-1] - stTimeList[0])
        stepLengthRegress = para[4] * stepFreq + para[5]

        print("Step Num is %d, Step Frequency is %.3f and Step Length is %.4f" % (stepNum, stepFreq, stepLengthRegress))

        pass


if __name__ == "__main__":
    # TODO: ***** -- ***** #
    controlFlag = 1 # 0 : Testing Demo, 1 : AiFiMatch
    showFlags = (True, True, False, False)
    secondAiFi = AiFiMatcher()
    if controlFlag == 0:
        pass
    elif controlFlag == 1:
        # TODO: *****-- ***** #
        # Performance VS. Step Length Error
        stepLengthErrorList = (0.0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5)
        headingErrorList = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        errorType = "step"
        # Performance VS. Heading Error
        # stepLengthErrorList = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        # headingErrorList = (0, 10, 15, 20, 25, 30, 35, 40, 45, 50)
        # errorType = "heading"

        rawDataArray = []
        # initial point and direction
        routeRotClockWise = "0"
        moveVector = (1.2, 1.7)
        # TODO: *****-- ***** #
        saveFlags = (False, False, False) # From 0 index
        rootDirectory = "./RawData/AiFiMatch/ErrorInfluence"
        dataBelongs = "t1"
        # TODO: *****-- ***** #
        trajectorySwitch = 1
        if trajectorySwitch == 1:
            # TODO: First trajectory of AiFiMatch
            rawDataArrayofFirst = [
                # (# The first one
                #     "./RawData/AiFiMatch/FirstTrajectory/20180302213401_acce.csv",
                #     "./RawData/AiFiMatch/FirstTrajectory/20180302213401_gyro.csv",
                #     "./RawData/AiFiMatch/FirstTrajectory/20180302213401_route.csv",
                # ),
                (# The second one(*)
                    "./RawData/AiFiMatch/FirstTrajectory/20180302213910_acce.csv",
                    "./RawData/AiFiMatch/FirstTrajectory/20180302213910_gyro.csv",
                    "./RawData/AiFiMatch/FirstTrajectory/20180302213910_wifi.csv",
                    "./RawData/AiFiMatch/FirstTrajectory/20180302213910_route.csv",
                ),
                (# The third one
                    "./RawData/AiFiMatch/FirstTrajectory/20180302214450_acce.csv",
                    "./RawData/AiFiMatch/FirstTrajectory/20180302214450_gyro.csv",
                    "./RawData/AiFiMatch/FirstTrajectory/20180302214450_wifi.csv",
                    "./RawData/AiFiMatch/FirstTrajectory/20180302214450_route.csv",
                ),
            ]
            # initial point and direction
            firstRouteRotClockWise = "0"
            firstMoveVector = (1.2, 1.7)
            rawDataArray.extend(rawDataArrayofFirst)
            routeRotClockWise = firstRouteRotClockWise
            moveVector = firstMoveVector
            dataBelongs = "t1"
        elif trajectorySwitch == 2:
            pass
        elif trajectorySwitch == 3:
            pass
        errorListInSensorError = []
        for i in range(min(len(stepLengthErrorList), len(headingErrorList))):
            slError4Test = stepLengthErrorList[i]
            headingError4Test = headingErrorList[i]
            errorBySteps = []
            for k in range(1):
                for j in range(len(rawDataArray)):
                    filePaths = rawDataArray[j]
                    # Load sensor data from files
                    acceTimeList, acceValueList = loadAcceData(filePaths[0], relativeTime=False)
                    gyroTimeList, gyroValueList = loadGyroData(filePaths[1], relativeTime=False)
                    wifiTimeList, wifiScanList = loadMovingWifi(filePaths[2])
                    # load real locations
                    locRealDF = pd.read_csv(filePaths[3])
                    locRealList = [(loc[0], loc[1]) for loc in locRealDF.values]

                    secondAiFi.onlineViterbi(acceTimeList, acceValueList,
                                             gyroTimeList, gyroValueList,
                                             wifiTimeList, wifiScanList,
                                             startingDirection=0.0,
                                             stepError=slError4Test,
                                             headingError=headingError4Test
                                             )
            print "Step Error ", slError4Test, " Heading Error ", headingError4Test, " Position Error: ", 0.0
        errorFilePath = "%s/aifi_error_%s_%s_%s.csv" % (rootDirectory, errorType, dataBelongs, time.strftime("%m%d"))
        print errorFilePath
    print("Done.")