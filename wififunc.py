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

def wifiStrAnalysis(wifiStr):
    """
    :param wifiStr: e.g. f4:cb:52:00:4e:68|-40;f4:cb:52:00:4e:64|-30;9c:21:6a:7f:bf:7c|-52
    :return: {"f4:cb:52:00:4e:68": -40, "f4:cb:52:00:4e:64": -30, "9c:21:6a:7f:bf:7c": -52}
    """
    wifiDict = {}
    wifiList = [wifiRecord.split("|") for wifiRecord in wifiStr.split(';')]
    for wifi in wifiList:
        wifiDict[wifi[0]]=float(wifi[1])
    return wifiDict


def eulerDistanceA(baseWifiDict, compWifiDict, wifiNum=8, wifiDefault=-100.0):
    """
    calculate the euler distance between test data and train data, while test data is baseline
    :param baseWifiDict: test wifi data
    :param compWifiDict: train wifi data
    :param wifiNum: the wifi numbers to calculate euler distance
    :param wifiDefault: wifi default value
    :return: euler distance
    """
    eulerDist = 0.0
    baseWifiList = sorted(baseWifiDict.iteritems(), key=lambda d: d[1], reverse=True)[0:wifiNum]
    for baseWifi in baseWifiList:
        baseID = baseWifi[0]
        baseValue = baseWifi[1]
        compValue = wifiDefault if not compWifiDict.has_key(baseID) else compWifiDict.get(baseID)
        eulerDist += math.pow(baseValue - compValue, 2)
    return math.sqrt(eulerDist)


if __name__ == "__main__":
    wifiInfoFir = "f4:cb:52:00:4e:68|-40;f4:cb:52:00:4e:64|-30;9c:21:6a:7f:bf:7c|-52"
    wifiInfoSec = "f4:cb:52:00:4e:68|-40;f4:cb:52:00:4e:64|-40;9c:21:6a:7f:bf:7c|-57"
    print(eulerDistanceA(wifiStrAnalysis(wifiInfoFir), wifiStrAnalysis(wifiInfoSec)))
    print("Done.")