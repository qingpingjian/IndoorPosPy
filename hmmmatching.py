#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/3/8 11:04
@author: Pete
@email: yuwp_1985@163.com
@file: hmmmatching.py
@software: PyCharm Community Edition
"""
from comutil import *
from abstractmap import *
from dataloader import loadAcceData, loadGyroData
from stepcounter import SimpleStepCounter
from turndetector import SimpleTurnDetector

class SegmentHMMMatcher(object):
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
                      startingDirection=0.0):
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
        stepLength = para[4] * stepFreq + para[5]
        print("Step Num is %d, Step Frequency is %.3f and Step Length is %.4f" % (stepNum, stepFreq, stepLength))

        # Detect Turns
        rotaValueList = rotationAngle(gyroTimeList, gyroValueList, normalize=False)
        rotaDegreeList = [r * 180.0 / math.pi for r in rotaValueList]
        windowSize = 23
        gyroTimeList, gyroValueList = slidingWindowFilter(gyroTimeList, gyroValueList, windowSize)
        simpleTd = SimpleTurnDetector(self.personID)
        turnIndexList, rtDegreeIndexList = simpleTd.detectTurn(gyroTimeList, gyroValueList, rotaDegreeList)

        #Map Matching based on steps and turns
        # First, initial candidates from initial direction
        candidateList = self.digitalMap.extractSegmentByDir(startingDirection)
        # Initial point estimation
        initPoint = np.mean([(segment[0], segment[1]) for segment in candidateList], axis=0)
        print("The initial point estimation is (%.3f, %.3f)" % (initPoint[0], initPoint[1]))



if __name__ == "__main__":
    sensorFilePath = ("./RawData/AiFiMatch/ThirdTrajectory/20180303143913_acce.csv",
                      "./RawData/AiFiMatch/ThirdTrajectory/20180303143913_gyro.csv",
                      "./RawData/AiFiMatch/ThirdTrajectory/20180303143913_wifi.csv")

    # Load sensor data from files
    acceTimeList, acceValueList = loadAcceData(sensorFilePath[0], relativeTime=False)
    gyroTimeList, gyroValueList = loadGyroData(sensorFilePath[1], relativeTime=False)

    firstMatcher = SegmentHMMMatcher()
    myDigitalMap = DigitalMap()
    firstMatcher.updateDigitalMap(myDigitalMap)

    initDirection = 0.0
    firstMatcher.onlineViterbi(acceTimeList, acceValueList, gyroTimeList, gyroValueList)

    print("Done.")