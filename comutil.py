#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/1/4 9:15
@author: Pete
@email: yuwp_1985@163.com
@file: comutil.py
@software: PyCharm Community Edition
"""
import math
import numpy as np
import scipy.signal as signal
import sys

from wififunc import wifiStrAnalysis

"""
: accelerometer peak threshold, valley threshold,
minimum two step peak duration, minimum duration between end and next start point
: step length slope and offset
: gyroscope peak threshold, valley threshold, minimum duration between two peak points,
minimum slope belongs to mainly turning progress, minimum degree change belongs to mainly turning progress,
maximum pause in turning progress, minimum degree for a left or right turn
"""
modelParameterDict = {
    "pete": (0.85, -0.20, 0.380, 0.175,
             0.28927316, 0.21706846,
             0.905, -0.905, 2.45, 15.0, 12.0, 1.725, 75.0),
    "super": (0.85, -0.20, 0.380, 0.175,
              0.21853894, 0.46235461,
              0.905, -0.905, 2.45, 15.0, 12.0, 1.725, 75.0)
}

def butterFilter(data, fs=50, lowcut=0.5, highcut=4.0, order=2):
    """
    Apply butterworth filter to the raw data
    :param data: raw data
    :param fs: sample frequency
    :param lowcut: low frequency threshold
    :param highcut: high frequency threshold
    :param order: butterworth band pass in  order value, 2 by default
    :return: filtered data
    """
    # butter band pass
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    dataArray = np.array(data).astype(np.float)
    y = signal.lfilter(b, a, dataArray)
    return y


def slidingWindowFilter(timeList, valueList, windowSize):
    midPos = (windowSize - 1) / 2
    currentIndex = 0
    dataLength = np.min((len(timeList), len(valueList)))
    timeFList = timeList[0:dataLength]
    valueFList = []
    valueFList.extend(valueList[currentIndex:currentIndex + midPos])
    valueFList.extend([np.mean(valueList[i - midPos : i + midPos + 1])
                       for i in range(currentIndex + midPos, dataLength - midPos)])
    valueFList.extend(valueList[dataLength - midPos:dataLength])
    return timeFList, valueFList


def getNextExtreme(valueList, startIndex=0, peakFlag=True, step=1):
    """
    Get the next peak point or valley point from the given start index at the given step
    :param valueList: one dimensional data list
    :param startIndex: the given start index
    :param peakFlag:  if this is True, we search peak point, otherwise, we search valley point
    :param step: {1, -1}, default 1, search forward, -1 search backward
    :return: the index and value of next extreme point
    """
    if startIndex + step * 2 >= len(valueList) or startIndex + step * 2 <= -1:
        return startIndex, None

    searchList = np.array(valueList[startIndex::step]) * (1 if peakFlag else -1)

    searchIndex = 0
    value = searchList[searchIndex]
    nextValue = searchList[searchIndex+1]
    while nextValue <= value:
        value = nextValue
        searchIndex = searchIndex + 1
        if searchIndex + 2 >= len(searchList):
            return startIndex + searchIndex * step, None
        nextValue = searchList[searchIndex + 1]
    while nextValue >= value:
        value = nextValue
        searchIndex = searchIndex + 1
        if searchIndex + 2 >= len(searchList):
            break
        nextValue = searchList[searchIndex + 1]
    extremeIndex = startIndex + searchIndex * step
    return extremeIndex, valueList[extremeIndex]


def varOfAcce(timeList, valueList, windowSize):
    midPos = (windowSize - 1) / 2
    votList = [timeList[i] for i in range(midPos, len(valueList) - midPos)]
    varList = [np.var(valueList[i - midPos:i + midPos + 1]) for i in range(midPos, len(valueList) - midPos)]
    return votList, varList


def angleNormalize(angle):
    """
    Keep angle in {0, 2pi)
    :param angle:
    :return: Normalized angle value
    """
    return (angle % (2.0 * math.pi) + 2.0 * math.pi) % (2.0 * math.pi)


def meanAngle(angleList, normalize = True):
    """
    Calculate the average of a set of circular data in radian
    :param angleList: a set of circular data
    :return: average value in radian
    """
    sinSum = 0
    cosSum = 0
    for angle in angleList:
        sinSum += math.sin(angle)
        cosSum += math.cos(angle)
    meanValue = math.atan2(sinSum, cosSum)
    return angleNormalize(meanValue) if normalize else meanValue


def rotationAngle(gyroTimeList, gyroValueList, normalize = True):
    """
    clockwise rotation return position values and keep rotation angle in {0, 2pi) based on normalize flag
    :param gyroTimeList: Gyroscope data timestamp
    :param gyroValueList: Gyroscope data list
    :param normalize: normalize flag
    :return: rotation angle in radian
    """
    # Between two timestamps, we use the average value as the real rate.
    avgList = [gyroValueList[0]]
    avgList.extend([(gyroValueList[i - 1] + gyroValueList[i]) / 2.0 for i in range(1, len(gyroValueList))])
    integrationList = [0.0]
    for j in range(1, len(avgList)):
        integrationList.append((gyroTimeList[j] - gyroTimeList[j - 1]) * avgList[j] + integrationList[j - 1])
    # clockwise rotation return position values and keep rotation angle in {0, 2pi) based on circularData flag
    return [angleNormalize(-1.0 * rot) if normalize else (-1.0 * rot) for rot in integrationList]


def timeAlign(baseTime, targetTimeList, startIndex = 0):
    """
    Get the index based on timestamp
    :param baseTime: According to this timestamp, we search the target timestamp index
    :param targetTimeList: Target timestamp List
    :param startIndex: start index
    :return: index of timestamp
    """
    targetIndex = startIndex
    if baseTime <= targetTimeList[startIndex]:
        targetIndex = startIndex
    elif baseTime >= targetTimeList[-1]:
        targetIndex = len(targetTimeList) - 1
    else:
        for i in range(startIndex + 1, len(targetTimeList)):
            if baseTime < targetTimeList[i]:
                targetIndex = i if targetTimeList[i] - baseTime < baseTime - targetTimeList[i - 1] else i - 1
                break
    return targetIndex


def wifiExtract(startTime, endTime, wifiTimeList, wifiScanList, startIndex=0):
    """
    Get Wi-Fi scan record according start timestamp and end timestamp
    :param startTime: start timestamp
    :param endTime:  end timestamp
    :param wifiTimeList:  wifi timestamp list
    :param wifiScanList:  Wi-Fi scan results list
    :param startIndex:  the starting searching index
    :return: nextIndex, {mac1:[rss1,rss2], mac2:[rss3, rss4]} or None
    """
    # check the input parameter
    if endTime <= startTime or wifiTimeList[startIndex] > endTime or wifiTimeList[-1] < startTime:
        return startIndex, None
    wifiRecordList = []
    nextIndex = startIndex
    for x in range(startIndex, len(wifiTimeList)):
        if wifiTimeList[x] >= startTime and wifiTimeList[x] <= endTime:
            wifiRecordList.append(wifiScanList[x])
            nextIndex = x + 1
            continue
        if wifiTimeList[x] > endTime:
            break
    return nextIndex, wifiStrAnalysis(wifiRecordList)


def locTransformR2W(relLoc, moveVector, rotStr):
    """
    Transform relative coordinate to world coordinate.
    First rotate the relative coordinate to world coordinate.
    Then move to the world origin point: moveVector + relLoc_Rotated
    :param relLoc: relative location
    :param moveVector: moving vector at world coordinate
    :param rotStr: clockwise rotation angle in degree
    :return: location at world coordinate
    """
    x = relLoc[0]
    y = relLoc[1]
    rotedLoc = (x, y)
    # clockwise rotation first
    if rotStr == "90":
        rotedLoc = (-y, x)
    elif rotStr == "180":
        rotedLoc = (-x, -y)
    elif rotStr == "270":
        rotedLoc = (y, -x)
    return (moveVector[0] + rotedLoc[0], moveVector[1] + rotedLoc[1])


def locTransformW2R(worldLoc, moveVector, rotStr):
    """
    Transform world coordinate to relative coordinate.
    First move to the relative origin point: worldLoc - moveVector
    Then rotate the world coordinate to relative coordinate.
    :param worldLoc: world location
    :param moveVector: moving vector at world coordinate
    :param rotStr: clockwise rotation angle in degree
    :return: location at relative coordinate
    """
    x = worldLoc[0] - moveVector[0]
    y = worldLoc[1] - moveVector[1]
    relLoc = (x, y)
    if rotStr == "90":
        relLoc = (-y, x)
    elif rotStr == "180":
        relLoc = (-x, -y)
    elif rotStr == "270":
        relLoc = (y, -x)
    return relLoc


def meanLocation(weightedLocList, weightedMean=True):
    """
    Calculate the mean location based on weighted parameter
    :param weightedLocList: [((x1, y1), w1), ((x2, y2), w2)]
    :param weightedMean: if this is true, we calculate mean values using weight parameters
    :return: mean location
    """
    weightList = np.ones(len(weightedLocList)) / len(weightedLocList)
    if weightedMean:
        weightList = np.array([wgtLoc[1] for wgtLoc in weightedLocList])
        weightList /= np.sum(weightList)
    xWeight = 0.0
    yWeight = 0.0
    for i in range(len(weightedLocList)):
        xWeight += weightedLocList[i][0][0] * weightList[i]
        yWeight += weightedLocList[i][0][1] * weightList[i]
    return (xWeight, yWeight)


def distError(realList, estiList):
    errorList = []
    for i in range(len(realList)):
        estiPoint = estiList[i] if i < len(estiList) else estiList[-1]
        realPoint = realList[i]
        errorList.append(math.sqrt(math.pow(estiPoint[0] - realPoint[0], 2) + math.pow(estiPoint[1] - realPoint[1], 2)))
    return errorList


def cdf(data, hasDuplicate=True):
    sortedData = np.sort(data)
    dataLength = len(sortedData)
    cdfData = np.arange(1, dataLength + 1) / float(dataLength)
    retValue = (sortedData, cdfData)
    if hasDuplicate:
        distinctData = [sortedData[-1]]
        distinctCDF = [1.0]
        for i in range(dataLength - 2, -1, -1):
            if math.fabs(distinctData[-1] - sortedData[i]) > sys.float_info.epsilon:
                distinctData.append(sortedData[i])
                distinctCDF.append(cdfData[i])
        retValue = (np.array(distinctData), np.array(distinctCDF))
    return retValue

if __name__ == "__main__":
    print("Done.")