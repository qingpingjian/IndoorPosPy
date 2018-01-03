#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2017/12/27 22:03
@author: Pete
@email: yuwp_1985@163.com
@file: stepcounter.py
@software: PyCharm Community Edition
"""

import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import string

from dataloader import butterFilter, loadAcceData


# Prepocess the acceleration data
def prepocessData(acceDataFilePath) :
    gravity = 9.411869 # Expect value of holding mobile phone static
    acceTimeReferenceList = []
    acceValueList = []
    with open(acceDataFilePath) as dataFile:
        reader = csv.DictReader(dataFile)
        for row in reader:
            acceTimeReferenceList.append(string.atof(row['Time(s)']))
            xAxis = string.atof(row['acce_x'])
            yAxis = string.atof(row['acce_y'])
            zAxis = string.atof(row['acce_z'])
            acceValueList.append(math.sqrt(math.pow(xAxis, 2) + math.pow(yAxis, 2) + math.pow(zAxis, 2)) - gravity)
        # Time axis in seconds
        acceTimeReferenceList = [(t - acceTimeReferenceList[0]) for t in acceTimeReferenceList]
    return acceTimeReferenceList, acceValueList


# # Apply butterworth filter to the raw accelerometer data
# def butterBandpass(lowcut, highcut, fs, order = 2):
#     nyq = 0.5 * fs
#     low = lowcut / nyq
#     high = highcut / nyq
#     b, a = signal.butter(order, [low, high], btype='band')
#     return b, a
# def butterFilter(data, lowcut, highcut, fs, order = 2):
#     b, a = butterBandpass(lowcut, highcut, fs, order=order)
#     y = signal.lfilter(b, a, data)
#     return y


# Calculate the average value of data list
# def averageValue(valueList, currentIndex, windowSize) :
#     middlePos = (windowSize - 1) / 2
#     startIndex = currentIndex - middlePos
#     if startIndex < 0 :
#         startIndex = 0
#     endIndex = currentIndex + middlePos
#     if endIndex > (len(valueList) - 1) :
#         endIndex = len(valueList) - 1
#     dataList = valueList[startIndex : endIndex]
#     sum = 0.0
#     for data in dataList :
#         sum = sum + data
#     sum = sum / len(dataList)
#     # Multiply a factor so the range will be larger between the bottom and the up
#     gravity = 9.50
#     sum = (sum - gravity) * (2.5) + gravity
#     sum = sum - gravity
#     return sum

# pointType - 1 peak, 2 trough
# def getNextExtremum(valueList, startIndex, pointType) :
#     index = startIndex
#     value = valueList[index]
#     nextValue = valueList[index + 1]
#     if pointType == 1 :
#         while nextValue <= value :
#             value = nextValue
#             index = index + 1
#             nextValue = valueList[index + 1]
#         while nextValue >= value :
#             value = nextValue
#             index = index + 1
#             nextValue = valueList[index + 1]
#     elif pointType == 2 :
#         while nextValue >= value :
#             value = nextValue
#             index = index + 1
#             nextValue = valueList[index + 1]
#         while nextValue <= value :
#             value = nextValue
#             index = index + 1
#             nextValue = valueList[index + 1]
#     return index, value


# pointType - 1 peak, 2 trough
def getNextExtremum(valueList, startIndex, pointType) :
    index = startIndex
    value = valueList[index]
    nextValue = valueList[index + 1]
    if pointType == 1 :
        while nextValue <= value :
            value = nextValue
            index = index + 1
            if index + 2 >= len(valueList):
                break
            nextValue = valueList[index + 1]
        while nextValue >= value :
            value = nextValue
            index = index + 1
            if index + 2 >= len(valueList):
                break
            nextValue = valueList[index + 1]
    elif pointType == 2 :
        while nextValue >= value :
            value = nextValue
            index = index + 1
            if index + 2 >= len(valueList):
                break
            nextValue = valueList[index + 1]
        while nextValue <= value :
            value = nextValue
            index = index + 1
            if index + 2 >= len(valueList):
                break
            nextValue = valueList[index + 1]
    return index, value


def stepCount(timeList, valueList, maxThreshold, timeThreshold) :
    peakTimeList = []
    peakValueList = []

    index = 0
    # The last 2 samples do not affect the step counting result
    while index < len(valueList) - 2 :
        value = valueList[index]
        if (value <= maxThreshold) :
            index = index + 1
            continue
        peakIndex, peakValue = getNextExtremum(valueList, index, 1)
        # Next index for our algorithm
        index = peakIndex + 1
        # Peak in the trough
        if peakValue <= maxThreshold :
            continue
        peakTime = timeList[peakIndex]
        if (len(peakValueList) == 0 or peakTime - peakTimeList[-1] >= timeThreshold) :
            peakValueList.append(peakValue)
            peakTimeList.append(peakTime)
        else :
            if peakValue >= peakValueList[-1] :
                peakValueList[-1] = peakValue
                peakTimeList[-1] = peakTime

    return peakTimeList, peakValueList


class SimpleStepCounter(object):

    def __init__(self, maxThreshold, minThreshold, timeThreshold):
        self.maxThreshold = maxThreshold
        self.minThreshold = minThreshold
        self.timeThreshold = timeThreshold

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
        :return: the peak point index and indexes of its start trough point and end trough point
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
            if len(peakValueList) == 0 or peakTime - peakTimeList[-1] >= self.timeThreshold:
                peakValueList.append(peakValue)
                peakTimeList.append(peakTime)
                peakIndexList.append(peakIndex)
            else:
                if peakValue >= peakValueList[-1]:
                    peakValueList[-1] = peakValue
                    peakTimeList[-1] = peakTime
                    peakIndexList[-1] = peakIndex
        # Now we need to find the start point and the end point of each step
        minThreshold = -0.1 # To exclude double peak situation
        stepIndexList = [] # start1, end1, start2, end2
        for i in range(len(peakValueList)):
            peakIndex = peakIndexList[i]
            startIndex = peakIndex - 1
            while(startIndex > 2):
                startIndex, startValue = self.searchTrough(valueList, startIndex, False)
                if startValue < minThreshold:
                    break
                startIndex = startIndex - 1
            endIndex = peakIndex + 1
            while(endIndex < len(valueList) - 2):
                endIndex, endValue = self.searchTrough(valueList, endIndex, 1)
                if endValue < minThreshold:
                    break
                endIndex = endIndex + 1
            if len(stepIndexList) > 0 and stepIndexList[-1] > startIndex:
                continue
            stepIndexList.append(startIndex)
            stepIndexList.append(endIndex)
        return stepIndexList

if __name__ == "__main__" :
    # Accelerometer data for step counting
    #acceDataFilePath = "./SensorData/20170511153750_acce.txt"
    acceDataFilePath = "./RawData/StepCounter/20170707201405_acce.txt"
    # Get accelerator data in txt file
    acceTimeReferenceList, acceValueList = prepocessData(acceDataFilePath)

    aTList, aVList = loadAcceData(acceDataFilePath)

    # Smoothing filter - sliding windows
    # size = 7
    # acceValueList = [averageValue(acceValueList, t, size) for t in range(len(acceValueList))]

    # Bandpass butterworth filter
    # Sample rate and desired cutoff frequencies (in Hz)
    sampleFs = 50 # sample by every 20ms
    lowCutOff = 0.5
    highCutOff = 4
    acceValueArray = np.array(acceValueList)
    acceValueArray = acceValueArray.astype(np.float)
    acceValueArrayF = butterFilter(acceValueList)

    avArray = np.array(aVList).astype(np.float)
    avArrayF = butterFilter(aVList)

    # Algorithm of step counter
    maxThreshold = 0.85      # m/s^2
    timeThreshold = 0.380     # s
    peakTimeList, peakValueList = stepCount(acceTimeReferenceList, acceValueArrayF,\
        maxThreshold, timeThreshold)
    print("Num of Step is: %d" % (len(peakValueList)))
    print("Peak values are below:")
    print(peakValueList)
    stepDuration = (peakTimeList[-1] - peakTimeList[0]) / (len(peakTimeList) - 1)
    print("One Step Duration is: %.3f and Step Frequency is: %.3f" % (stepDuration, 1.0/stepDuration))
    # Plot the axes
    plt.xlabel(r"$time(s)$", fontsize=25)
    plt.ylabel(r"$acceleration(m/s^2)$", fontsize=25)
    acceLine, = plt.plot(acceTimeReferenceList, acceValueArrayF, lw=3,color="red", label="Acceleration")
    acceLine2, = plt.plot(aTList, avArrayF, lw=1, color = "blue", label="Acceleration Panda")
    stepMarker, = plt.plot(peakTimeList, peakValueList, "rx", ms=10, label="Steps")
    plt.legend(handles=[acceLine, acceLine2, stepMarker], fontsize=20)
    plt.show()
    print("Done.")