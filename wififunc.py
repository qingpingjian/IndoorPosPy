#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2017/11/10 上午1:00
@author: Pete
@email: yuwp_1985@163.com
@file: wififunc.py
@software: PyCharm Community Edition
"""

import math
import numpy as np

from scipy import stats

def wifiStrAnalysis(wifiStrList):
    """
    :param wifiStrList: e.g. [f4:cb:52:00:4e:68|-40;f4:cb:52:00:4e:64|-30;9c:21:6a:7f:bf:7c|-52]
    :return: {"f4:cb:52:00:4e:68": [-40], "f4:cb:52:00:4e:64": [-30], "9c:21:6a:7f:bf:7c": [-52]}
    """
    if len(wifiStrList) == 0:
        return None
    wifiDict = {}
    for wifiStr in wifiStrList:
        wifiList = [wifiRecord.split("|") for wifiRecord in wifiStr.split(';')]
        for wifi in wifiList:
            if wifiDict.has_key(wifi[0]):
                wifiDict.get(wifi[0]).append(float(wifi[1]))
            else:
                wifiDict[wifi[0]]=[float(wifi[1])]
    return wifiDict


def wifiDict2Str(wifiDict):
    wifiStrList = ["%s|%.1f" % (mac, float(np.mean(rssList))) for mac, rssList in wifiDict.iteritems()]
    return ";".join(wifiStrList)


def combineWifiDict(firstWifiDict, secondWifiDict):
    macSet = set(firstWifiDict.keys()+secondWifiDict.keys())
    wifiDictNew = {}
    for mac in macSet:
        if firstWifiDict.has_key(mac) and secondWifiDict.has_key(mac):
            wifiDictNew[mac] = firstWifiDict.get(mac) + secondWifiDict.get(mac) # connect two list
        elif firstWifiDict.has_key(mac):
            wifiDictNew[mac] = firstWifiDict.get(mac)
        else:
            wifiDictNew[mac] = secondWifiDict.get(mac)
    return wifiDictNew


def eulerDistanceA(baseWifiDict, compWifiDict, wifiNum=7, wifiDefault=-100.0):
    """
    calculate the euler distance between test data and train data, while test data is baseline
    :param baseWifiDict: test wifi data
    :param compWifiDict: train wifi data
    :param wifiNum: the wifi numbers to calculate euler distance
    :param wifiDefault: default rss value if we do not receive the signal
    :return: euler distance
    """
    eulerDist = 0.0
    baseWifiList = sorted(baseWifiDict.iteritems(), key=lambda d: np.mean(d[1]), reverse=True)[0:wifiNum]
    for baseWifi in baseWifiList:
        baseID = baseWifi[0]
        baseValue = baseWifi[1]
        compValue = wifiDefault if not compWifiDict.has_key(baseID) else compWifiDict.get(baseID)
        eulerDist += math.pow(np.mean(baseValue) - np.mean(compValue), 2)
    return math.sqrt(eulerDist)


def jaccardDist(firstWifiDict, secondWifiDict):
    # TODO: for rss value is very small, the AP should be excluded
    firstMacSet = set(firstWifiDict.keys())
    secondMacSet = set(secondWifiDict.keys())
    unionSet = firstMacSet | secondMacSet
    interSet = firstMacSet & secondMacSet
    jcd = (len(unionSet) - len(interSet)) * 1.0 / len(unionSet)
    return jcd


def bayesProbability(baseWifiDict, compGaussianDict, wifiNum=7, wifiDefault=-100.0):
    """
    calculate the log gassian probability of test data comparing with train data
    :param baseWifiDict: test wifi data
    :param compGaussianDict: train wifi distribution parameters
    :param wifiNum: the wifi numbers to calculate bayes probability
    :param wifiDefault: default rss value if we do not receive the signal
    :return: bayes probability
    """
    logGaussian = 0.0
    baseWifiList = sorted(baseWifiDict.iteritems(), key=lambda d: np.mean(d[1]), reverse=True)[0:wifiNum]
    for baseWifi in baseWifiList:
        baseID = baseWifi[0]
        baseValue = np.mean(baseWifi[1])
        meanValue, stdValue = compGaussianDict.get(baseID) if compGaussianDict.has_key(baseID) else (wifiDefault, 3.0)
        logGaussian += stats.norm.logpdf(baseValue, loc=meanValue, scale=stdValue)
    # math.exp(logGaussian) is too small
    return logGaussian


def wifiSequenceProcess(wifiSequence):
    xLocList = [wifi[0] for wifi in wifiSequence]
    yLocList = [wifi[1] for wifi in wifiSequence]
    xDistance = np.max(xLocList) - np.min(xLocList)
    yDistance = np.max(yLocList) - np.min(yLocList)
    # Sorted the locations by x coordinate
    if xDistance > yDistance:
        wifiSequence.sort(key=lambda wifi : wifi[0])
    else: # Sorted the locations by y coordinate
        wifiSequence.sort(key=lambda  wifi : wifi[1])
    # combine two fingerprints if they are close to each other
    seqLeng = len(wifiSequence)
    wifiSeqNew = []
    i = 0
    while i < seqLeng:
        refWifi = wifiSequence[i]
        j = i + 1
        while j < seqLeng:
            secWifi = wifiSequence[j]
            if math.sqrt((secWifi[0] - refWifi[0]) ** 2 + (secWifi[1] - refWifi[1]) ** 2) > 0.1:
                break
            refWifi = ((secWifi[0]+refWifi[0])/2, (secWifi[1]+refWifi[1])/2, combineWifiDict(refWifi[2], secWifi[2]))
            j += 1
        i = j
        wifiSeqNew.append(refWifi)
    return wifiSeqNew


def wifiSeqJaccardDist(baseWifiSeq, walkWifiSeq, windowSize=3):
    if len(baseWifiSeq) < 5 or len(walkWifiSeq) < 3:
        return 1.0 * windowSize
    jcd = 1.0 * windowSize
    firstSeq = baseWifiSeq
    secondSeq = walkWifiSeq
    if len(baseWifiSeq) < len(walkWifiSeq):
        firstSeq = walkWifiSeq
        secondSeq = baseWifiSeq
    # In the proper order
    for i in range(0, len(firstSeq)-len(secondSeq)+1):
        jcdSum = 0.0
        for j in range(0, len(secondSeq)):
            jcdSum += jaccardDist(secondSeq[j][2], firstSeq[i+j][2])
        jcdSum /= len(secondSeq)
        jcd = min(jcd, jcdSum)
    # In the opposite order
    for i in range(len(firstSeq)-1, len(secondSeq)-2, -1):
        jcdSum = 0.0
        for j in range(0, len(secondSeq)):
            jcdSum += jaccardDist(secondSeq[j][2], firstSeq[i-j][2])
        jcdSum /= len(secondSeq)
        jcd = min(jcd, jcdSum)
    return jcd


if __name__ == "__main__":
    wifiInfoFir = "f4:cb:52:00:4e:68|-40;f4:cb:52:00:4e:64|-30;9c:21:6a:7f:bf:7c|-52"
    wifiInfoSec = "f4:cb:52:00:4e:68|-40;f4:cb:52:00:4e:64|-40;9c:21:6a:7f:bf:7c|-57"
    wifiInfoThd = "f4:cb:52:00:4e:68|-40;f4:cb:52:00:4e:65|-40;9c:21:6a:7f:bf:7c|-53"
    print(jaccardDist(wifiStrAnalysis([wifiInfoFir]), wifiStrAnalysis([wifiInfoSec])))
    print(jaccardDist(wifiStrAnalysis([wifiInfoFir]), wifiStrAnalysis([wifiInfoThd])))
    print("Done.")