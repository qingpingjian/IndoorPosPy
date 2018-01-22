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
from dataloader import loadGyroData

matplotlib.rcParams['axes.unicode_minus'] = False # Show minus normally

class SimpleTurnDetector(object):

    def __init__(self, upperThreshold, lowerThreshold, durationThreshold, intervalThreshold):
        self.upperTd = upperThreshold   # radian/s
        self.lowerTd = lowerThreshold   # radian/s
        self.durationTd = durationThreshold # seconds
        self.intervalTd = intervalThreshold # seconds
        pass

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
        turnIndexList = []
        turnIndexList.extend(peakIndexList)
        turnIndexList.extend(valleyIndexList)
        return sorted(turnIndexList)

    def detectTurn(self, timeList, valueList):

        pass

if __name__ == "__main__":
    sensorFilePath = ("./Examples/ActivityDetector/20170702210514_acce.csv",
                      "./Examples/ActivityDetector/20170702210514_gyro.csv")
    gyroTimeList, gyroValueList = loadGyroData(sensorFilePath[1])
    rotaValueList = rotationAngle(gyroTimeList, gyroValueList, normalize=False)

    windowSize = 23
    gyroTimeList, gyroValueList = slidingWindowFilter(gyroTimeList, gyroValueList, windowSize)

    para = modelParameterDict.get("pete")

    simpleTd = SimpleTurnDetector(para[6], para[7], para[8], para[9])
    turnIndexList = simpleTd.turnPoint(gyroTimeList, gyroValueList)

    # Turn point time and value
    turnTimeList = [gyroTimeList[i] for i in turnIndexList]
    turnValueList = [gyroValueList[i] for i in turnIndexList]

    # Plot the figures
    fig = plt.figure()
    gyroRateAxes = fig.add_subplot(111)
    rotaAngleAxes = gyroRateAxes.twinx()

    gyroRateAxes.set_xlabel("$Time(s)$")
    gyroRateAxes.set_ylabel("$Rotation Rate(radian/s)$")
    # gyroRateAxes.set_xticklabels(np.array(np.linspace(0, 30, 7), np.int))
    # gyroRateAxes.set_yticklabels(np.linspace(-1.5, 1.5, 7))
    ratePlot, = gyroRateAxes.plot(gyroTimeList, gyroValueList, color="g", label="Rotation Rate")
    for i in range(len(turnTimeList)):
        gyroRateAxes.axvline(turnTimeList[i], ls="--", lw=2, color="r")
    print("We find %d turns" % (len(turnIndexList)))
    # gyroRateAxes.yaxis.label.set_color(ratePlot.get_color())

    rotaAngleAxes.set_ylabel("$Rotation(degree)$")
    # rotaAngleAxes.set_yticklabels(np.array(np.linspace(-100, 20, 7), np.int))
    anglePlot, = rotaAngleAxes.plot(gyroTimeList, [r * 180.0 / math.pi for r in rotaValueList], color="b", linestyle="--", label="Rotation Angle")
    # rotaAngleAxes.yaxis.label.set_color(anglePlot.get_color())

    plt.legend(handles=[ratePlot, anglePlot], loc=4)
    plt.show()

    print("Done.")