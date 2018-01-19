#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2017/12/27 22:03
@author: Pete
@email: yuwp_1985@163.com
@file: stepcounter.py
@software: PyCharm Community Edition
"""

import math
import matplotlib.pyplot as plt

from comutil import butterFilter, modelParameterDict
from dataloader import loadAcceData


class SimpleStepCounter(object):

    def __init__(self, maxThreshold, minThreshold, durationThreshold, intervalThreshold):
        self.maxThreshold = maxThreshold
        self.minThreshold = minThreshold
        self.durationThreshold = durationThreshold
        self.intervalThreshold = intervalThreshold

    def getNextPeak(self, valueList, startIndex):
        """
        Get the next peak point from the given start index, startIndex <= len(valueList) - 2
        :param valueList: accelerometer data list
        :param startIndex: the given start index
        :return: the index and value of next peak point
        """
        index = startIndex
        value = valueList[index]
        nextValue = valueList[index + 1]
        while nextValue <= value :
            value = nextValue
            index = index + 1
            if index + 2 >= len(valueList):
                return index, value # Can not find a valid peak
            nextValue = valueList[index + 1]
        while nextValue >= value :
            value = nextValue
            index = index + 1
            if index + 2 >= len(valueList):
                break
            nextValue = valueList[index + 1]
        return index, value

    def searchTrough(self, valueList, startIndex, direction = True):
        """
        If direction is True, we search the next trough, otherwise we search the previous trough
        :param valueList: accelerometer data list
        :param startIndex: the given start index
        :param direction: the search direction flag
        :return: the index and value of wanted trough point
        """
        index = startIndex
        value = valueList[index]
        nextIndex = index + 1 if direction else index - 1
        nextValue = valueList[nextIndex]
        while nextValue <= value:
            value = nextValue
            index = nextIndex
            if (direction and index + 2 >= len(valueList)) or (not direction and index - 1 <= 0):
                break
            nextIndex = index + 1 if direction else index - 1
            nextValue = valueList[nextIndex]
        return index, value

    def countStep(self, timeList, valueList):
        """
        Get the step count from the given accelerometer data
        :param timeList: time list of accelerometer
        :param valueList: accelerometer data list
        :return: start trough point, peak point and end trough point indexes of each step
        """
        peakTimeList = []
        peakValueList = []
        peakIndexList = []
        index = 0
        # The last 2 samples do not affect the step counting result
        while index < len(valueList) - 2:
            value = valueList[index]
            # We want to find peak value fast
            if value <= self.maxThreshold:
                index += 1
                continue
            peakIndex, peakValue = self.getNextPeak(valueList, index)
            # Next index for our algorithm
            index = peakIndex + 1
            # Peak in the trough
            if peakValue <= self.maxThreshold:
                continue
            peakTime = timeList[peakIndex]
            if len(peakValueList) == 0 or peakTime - peakTimeList[-1] >= self.durationThreshold:
                peakValueList.append(peakValue)
                peakTimeList.append(peakTime)
                peakIndexList.append(peakIndex)
            else:
                if peakValue >= peakValueList[-1]:
                    peakValueList[-1] = peakValue
                    peakTimeList[-1] = peakTime
                    peakIndexList[-1] = peakIndex
        # Now we need to find the start point and the end point of each step
        stepIndexList = [] # start1, end1, start2, end2
        for i in range(len(peakValueList)):
            peakIndex = peakIndexList[i]
            startIndex = peakIndex - 1
            while startIndex > 2:
                startIndex, startValue = self.searchTrough(valueList, startIndex, False)
                if startValue < self.minThreshold:  # To exclude double peak situation
                    break
                startIndex -= 1
            endIndex = peakIndex + 1
            while endIndex < len(valueList) - 2:
                endIndex, endValue = self.searchTrough(valueList, endIndex)
                if endValue < self.minThreshold:  # To exclude double peak situation
                    break
                endIndex += 1
            # To conbine two consecutive steps, the last end index is the current start index
            if len(stepIndexList) > 0 and stepIndexList[-1] != startIndex and \
                    math.fabs(timeList[startIndex] - timeList[stepIndexList[-1]]) <= self.intervalThreshold:
                lastEndValue = valueList[stepIndexList[-1]]
                currentStartValue = valueList[startIndex]
                if lastEndValue < currentStartValue:
                    startIndex = stepIndexList[-1]
                else:
                    stepIndexList[-1] = startIndex
            stepIndexList.append(startIndex)
            stepIndexList.append(peakIndex)
            stepIndexList.append(endIndex)
        return stepIndexList


if __name__ == "__main__" :
    # Accelerometer data for step counting
    acceDataFilePath = "./Examples/StepCounter/20170707201405_acce.csv"

    acceTimeList, acceValueList = loadAcceData(acceDataFilePath)

    # Smoothing filter - sliding windows
    # size = 7
    # acceValueList = [averageValue(acceValueList, t, size) for t in range(len(acceValueList))]

    acceValueArray = butterFilter(acceValueList)

    para = modelParameterDict.get("pete")
    # Algorithm of step counter
    sc = SimpleStepCounter(para[0], para[1], para[2], para[3])
    allIndexList = sc.countStep(acceTimeList, acceValueArray)

    # Transform from milliseconds to seconds
    acceTimeList = [t / 1000.0 for t in acceTimeList]

    peakIndexList = allIndexList[1::3]
    peakTimeList = [acceTimeList[i] for i in peakIndexList]
    peakValueList = [acceValueArray[i] for i in peakIndexList]
    stIndexList = allIndexList[0::3]
    stTimeList = [acceTimeList[i] for i in stIndexList]
    stValueList = [acceValueArray[i] for i in stIndexList]
    edIndexList = allIndexList[2::3]
    edTimeList = [acceTimeList[i] for i in edIndexList]
    edValueList = [acceValueArray[i] for i in edIndexList]

    print("Num of Step is: %d" % (len(peakIndexList)))
    print("Peak values are below:")
    print(peakValueList)

    # Plot the axes
    plt.xlabel("$time(s)$")
    plt.ylabel("$acceleration(m/s^2)$")
    acceLine, = plt.plot(acceTimeList, acceValueArray, lw=1,color="blue", label="Acceleration")
    stepPeaker, = plt.plot(peakTimeList, peakValueList, "rx", ms=10, label="Step Peaks")
    stepStarter, = plt.plot(stTimeList, stValueList, "yx", ms=8, label="Step Starts")
    stepEnder, = plt.plot(edTimeList, edValueList, "gx", ms=5, label="Step Ends")
    plt.legend(handles=[acceLine, stepPeaker, stepStarter, stepEnder], fontsize=20)
    plt.show()
    print("Done.")