#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/1/22 15:56
@author: Pete
@email: yuwp_1985@163.com
@file: turndetector.py
@software: PyCharm Community Edition
"""

import matplotlib
import matplotlib.pyplot as plt

from comutil import *
from dataloader import loadAcceData, loadGyroData

matplotlib.rcParams['axes.unicode_minus'] = False # Show minus normally

class SimpleTurnDetector(object):

    def __init__(self, upperThreshold=0.905, lowerThreshold=-0.905, durationThreshold=2.45,
                 minSlope=15.0, minRotDegree=12.0, maxPause=1.725, minTurnDegree=75.0):
        # parameters for turning point finding algorithm
        self.upperTd = upperThreshold   # radian/s
        self.lowerTd = lowerThreshold   # radian/s
        self.durationTd = durationThreshold # seconds
        # parameters for turning degree detection algorithm
        self.minSlope = minSlope    # degree/s
        self.minRotDegree = minRotDegree    # degree
        self.maxPause = maxPause    # seconds
        self.minTurnDegree = minTurnDegree

    def turnPoint(self, timeList, valueList):
        # First, find peak points to find turning left and turning around left
        currentIndex = 0
        peakIndexList = []
        peakValueList = []
        peakTimeList = []
        # The last 2 samples do not affect the step counting result
        while currentIndex < len(valueList) - 2:
            currentValue = valueList[currentIndex]
            if currentValue < self.upperTd:
                currentIndex += 1
                continue
            peakIndex, peakValue = getNextExtreme(valueList, currentIndex)
            if peakValue == None:
                break
            currentIndex = peakIndex + 1
            if peakValue < self.upperTd:
                continue
            peakTime = timeList[peakIndex]
            if len(peakValueList) == 0 or peakTime - peakTimeList[-1] >= self.durationTd:
                peakValueList.append(peakValue)
                peakTimeList.append(peakTime)
                peakIndexList.append(peakIndex)
            else:
                if peakValue >= peakValueList[-1]:
                    peakValueList[-1] = peakValue
                    peakTimeList[-1] = peakTime
                    peakIndexList[-1] = peakIndex
        # Second, find valley points to find turning right and turning around right
        currentIndex = 0
        valleyIndexList = []
        valleyValueList = []
        valleyTimeList = []
        # The last 2 samples do not affect the step counting result
        while currentIndex < len(valueList) - 2:
            currentValue = valueList[currentIndex]
            if currentValue > self.lowerTd:
                currentIndex += 1
                continue
            valleyIndex, valleyValue = getNextExtreme(valueList, currentIndex, peakFlag=False)
            if valleyValue == None:
                break
            currentIndex = valleyIndex + 1
            if valleyValue > self.lowerTd:
                continue
            valleyTime = timeList[valleyIndex]
            if len(valleyValueList) == 0 or valleyTime - valleyTimeList[-1] >= self.durationTd:
                valleyValueList.append(valleyValue)
                valleyTimeList.append(valleyTime)
                valleyIndexList.append(valleyIndex)
            else:
                if valleyValue <= valleyValueList[-1]:
                    valleyValueList[-1] = valleyValue
                    valleyTimeList[-1] = valleyTime
                    valleyIndexList[-1] = valleyIndex
        turnPointIndexList = []
        turnPointIndexList.extend(peakIndexList)
        turnPointIndexList.extend(valleyIndexList)
        return sorted(turnPointIndexList)

    def turnDegree(self, timeList, rotaDegreeList, startIndex, endIndex):
        # Find all extreme points (Peak and Valley)
        extremeIndexList = []
        currentIndex = startIndex
        while currentIndex < endIndex - 1:
            index, value = getNextExtreme(rotaDegreeList, currentIndex, peakFlag=True)
            extremeIndexList.append(index)
            currentIndex = index + 1
        currentIndex = startIndex
        while currentIndex < endIndex - 1:
            index, value = getNextExtreme(rotaDegreeList, currentIndex, peakFlag=False)
            extremeIndexList.append(index)
            currentIndex = index + 1
        extremeIndexList = sorted(extremeIndexList)
        # Find the turn start point and end point by gradient
        extremeTimeList = [timeList[i] for i in extremeIndexList]
        extremeValueList = [rotaDegreeList[i] for i in extremeIndexList]
        turnIndexList = []
        for i in range(1, len(extremeIndexList)):
            # gradient = (a - b) / (c - d)
            a = extremeValueList[i]
            b = extremeValueList[i-1]
            c = extremeTimeList[i]
            d = extremeTimeList[i-1]
            g = math.fabs((a - b) / (c - d))
            if g > self.minSlope and math.fabs(a - b) > self.minRotDegree:
                tsIndex = extremeIndexList[i-1]
                teIndex = extremeIndexList[i]
                if len(turnIndexList) == 0:
                    turnIndexList.append(tsIndex)
                    turnIndexList.append(teIndex)
                else:
                    lastEnd = turnIndexList[-1]
                    lastStart = turnIndexList[-2]
                    currentStart = tsIndex
                    if timeList[currentStart] - timeList[lastEnd] < self.maxPause:
                        turnIndexList[-1] = teIndex
                    elif math.fabs(rotaDegreeList[lastEnd] - rotaDegreeList[lastStart]) < self.minTurnDegree:
                        turnIndexList[-2] = tsIndex
                        turnIndexList[-1] = teIndex
                    else: # Now we have finded the turning start point and end point
                        break
        return turnIndexList

    def detectTurn(self, timeList, gyroValueList, rotaDegreeList):
        turnPointIndexList = self.turnPoint(timeList, gyroValueList)
        stAndedList = []
        for i in range(len(turnPointIndexList)):
            pointIndex = turnPointIndexList[i]
            # For each turn point, we give a start index and end index to search the rotation degree
            searchStIndex = max(0, pointIndex - 150)
            searchEdIndex = min(len(timeList)-1, pointIndex + 150)
            if i >= 1:
                searchStIndex = (pointIndex + turnPointIndexList[i-1]) / 2
            if i < len(turnPointIndexList)-1:
                searchEdIndex = (pointIndex + turnPointIndexList[i+1]) / 2
            turnIndexList = self.turnDegree(timeList, rotaDegreeList, searchStIndex, searchEdIndex)
            if len(turnIndexList) == 2:
                stAndedList.extend(turnIndexList)
            else:
                print("Something wrong happened!")
        return turnPointIndexList, stAndedList

    def turnTranslate(self, degree):
        turnName = "Unknown Turn"
        if degree >= self.minTurnDegree * 2:
            turnName = "Right Around"
        elif degree > self.minTurnDegree:
            turnName = "Turn Right"
        elif degree > self.minTurnDegree * -2 and degree < self.minTurnDegree:
            turnName = "Turn Left"
        elif degree <= self.minTurnDegree * -2:
            turnName = "Left Around"
        return turnName

if __name__ == "__main__":
    sensorFilePath = ("./Examples/ActivityDetector/20170702210514_acce.csv",
                      "./Examples/ActivityDetector/20170702210514_gyro.csv")
    acceTimeList, acceValueList = loadAcceData(sensorFilePath[0])
    acceValueArray = butterFilter(acceValueList)
    gyroTimeList, gyroValueList = loadGyroData(sensorFilePath[1])
    rotaValueList = rotationAngle(gyroTimeList, gyroValueList, normalize=False)
    rotaDegreeList = [r * 180.0 / math.pi for r in rotaValueList]

    windowSize = 23
    gyroTimeList, gyroValueList = slidingWindowFilter(gyroTimeList, gyroValueList, windowSize)

    para = modelParameterDict.get("pete")
    simpleTd = SimpleTurnDetector(upperThreshold=para[6], lowerThreshold=para[7], durationThreshold=para[8],
                                  minSlope=para[9], minRotDegree=para[10], maxPause=para[11], minTurnDegree=para[12])
    turnIndexList, rtDegreeIndexList = simpleTd.detectTurn(gyroTimeList, gyroValueList, rotaDegreeList)

    # Turn point time and value
    turnTimeList = [gyroTimeList[i] for i in turnIndexList]
    turnValueList = [gyroValueList[i] for i in turnIndexList]
    rtTimeList = [gyroTimeList[i] for i in rtDegreeIndexList]
    rtValueList = [rotaDegreeList[i] for i in rtDegreeIndexList]

    # Plot the figures
    fig = plt.figure()
    gyroRateAxes = fig.add_subplot(111)
    rotaAngleAxes = gyroRateAxes.twinx()

    gyroRateAxes.set_xlabel("$Time(s)$")
    gyroRateAxes.set_ylabel("$Rotation Rate(radian/s)$")
    # gyroRateAxes.set_xticklabels(np.array(np.linspace(0, 30, 7), np.int))
    # gyroRateAxes.set_yticklabels(np.linspace(-1.5, 1.5, 7))
    ratePlot, = gyroRateAxes.plot(gyroTimeList, gyroValueList, color="g", label="Rotation Rate")
    for t in turnTimeList:
        gyroRateAxes.axvline(t, ls="--", lw=2, color="r")
    print("We find %d turns" % (len(turnIndexList)))
    accePlot, = gyroRateAxes.plot(acceTimeList, acceValueArray, color="y", label="Accelerometer")
    # gyroRateAxes.yaxis.label.set_color(ratePlot.get_color())

    rotaAngleAxes.set_ylabel("$Rotation(degree)$")
    # rotaAngleAxes.set_yticklabels(np.array(np.linspace(-100, 20, 7), np.int))
    anglePlot, = rotaAngleAxes.plot(gyroTimeList, rotaDegreeList, color="b", linestyle="--", label="Rotation Angle")
    for t in rtTimeList:
        rotaAngleAxes.axvline(t, ls=":", lw=2, color="#FF00CC")
    print("Turns happen at:")
    for i in range(0, len(rtTimeList), 2):
        print("%s Start: %.3f and End: %.3f" % (simpleTd.turnTranslate(rtValueList[i+1] - rtValueList[i]),
                                                rtTimeList[i], rtTimeList[i+1]))
    # rotaAngleAxes.yaxis.label.set_color(anglePlot.get_color())

    plt.legend(handles=[ratePlot, accePlot, anglePlot], loc=4)
    plt.show()

    print("Done.")