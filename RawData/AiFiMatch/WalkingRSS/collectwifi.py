#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/5/7 16:31
@author: Pete
@email: yuwp_1985@163.com
@file: collectwifi.py
@software: PyCharm Community Edition
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from comutil import *
from dataloader import loadAcceData, loadMovingWifi
from stepcounter import SimpleStepCounter
from wififunc import wifiDict2Str, wifiSequenceProcess

# Environment Configuration
# matplotlib.rcParams['font.size'] = 15
# matplotlib.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签
matplotlib.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

def wifiSequence(priorInfo, sensorFiles, personID="pete", device="360n5", debugFlag=False):
    acceTimeList, acceValueList = loadAcceData(sensorFiles[0], relativeTime=False, deviceID=device)
    wifiTimeList, wifiScanList = loadMovingWifi(sensorFiles[1])

    # Count step
    acceValueArray = butterFilter(acceValueList)
    # Algorithm of step counter
    sc = SimpleStepCounter(personID)
    allIndexList = sc.countStep(acceTimeList, acceValueArray)
    wifiList = []

    # For debugging
    if debugFlag:
        stIndexList = allIndexList[0::3]
        stTimeList = [acceTimeList[i] for i in stIndexList]
        stValueList = [acceValueArray[i] for i in stIndexList]
        pkIndexList = allIndexList[1::3]
        pkTimeList = [acceTimeList[i] for i in pkIndexList]
        pkValueList = [acceValueArray[i] for i in pkIndexList]
        print "The average of peak values is ", np.mean(pkValueList)
        edIndexList = allIndexList[2::3]
        edTimeList = [acceTimeList[i] for i in edIndexList]
        edValueList = [acceValueArray[i] for i in edIndexList]
        stepNum = len(pkTimeList)
        print "Step number is ", stepNum
        print "Peak value at last", pkValueList[-1], "Peak value at first", pkValueList[0]
        print "The last duration is ", stTimeList[-1] - edTimeList[-2]
        # Plot the axes
        plt.xlabel("$time(s)$")
        plt.ylabel("$acceleration(m/s^2)$")
        acceLine, = plt.plot(acceTimeList, acceValueArray, lw=1, color="blue", label="Acceleration")
        stepPeaker, = plt.plot(pkTimeList, pkValueList, "rx", ms=10, label="Step Peaks")
        stepStarter, = plt.plot(stTimeList, stValueList, "yx", ms=8, label="Step Starts")
        stepEnder, = plt.plot(edTimeList, edValueList, "gx", ms=5, label="Step Ends")
        plt.legend(handles=[acceLine, stepPeaker, stepStarter, stepEnder], fontsize=20)
        plt.show()
    else:
        pkIndexList = allIndexList[1::3]
        pkTimeList = [acceTimeList[i] for i in pkIndexList]
        stepNum = min(priorInfo[2], len(pkIndexList))
        sp = priorInfo[0]
        ep = priorInfo[1]
        locList = genLocation(sp, ep, stepNum)
        # log information
        # print "Location number: ", len(locList), " and step number: ", stepNum

        # len(locList) = stepNum + 1
        currentWifiIndex = 0
        for i in range(len(locList)):
            startWifiTime = pkTimeList[i-1] if i >= 1 else 0
            endWifiTime = pkTimeList[i] if i < len(locList) - 1 else -1
            currentWifiIndex, currentWifiDict = wifiExtract(startWifiTime, endWifiTime, wifiTimeList, wifiScanList,
                                                            currentWifiIndex)
            if currentWifiDict == None:
                continue
            locNow = locList[i]
            wifiList.append((locNow[0], locNow[1], currentWifiDict))

    return wifiList


if __name__ == "__main__":
    saveFlags = (True, False)
    # 0 : tra01 & 360n5 & radiomap
    controlFlag = 0
    if controlFlag == 0:
        # TODO: Trajectory one radio map, (DONE)
        sensorFilesArray = (
            ("20180508085745_acce.csv", "20180508085745_wifi.csv"),
            ("20180508085831_acce.csv", "20180508085831_wifi.csv"),
            ("20180508163245_acce.csv", "20180508163245_wifi.csv"),
            ("20180508163330_acce.csv", "20180508163330_wifi.csv"),
            ("20180508163449_acce.csv", "20180508163449_wifi.csv"),
            ("20180508163535_acce.csv", "20180508163535_wifi.csv"),
        )
        # Starting points and end points, step numbers
        priorInfoArray = (
            ((49.8, 10.7), (1.2, 10.7), 63),  # 5745
            ((1.2, 10.7), (49.8, 10.7), 60),  # 5831
            ((49.8, 10.7), (1.2, 10.7), 63),  # 3245
            ((1.2, 10.7), (49.8, 10.7), 64),  # 3330
            ((49.8, 10.7), (1.2, 10.7), 61),  # 3449
            ((1.2, 10.7), (49.8, 10.7), 63),  # 3535
        )
        targetFile = "20180508163535_wifi_crowd.csv"
        wifiBoundList = []
        for i in range(len(sensorFilesArray)):
            wifiBoundList.extend(wifiSequence(priorInfoArray[i], sensorFilesArray[i]))
        wifiSequence = wifiSequenceProcess(wifiBoundList)
        if saveFlags[0]:
            wifiSeq2Save = [("tra01", round(wifi[0] * 1000) / 1000, round(wifi[1] * 1000) / 1000, wifiDict2Str(wifi[2])) for wifi in wifiSequence]
            wifiSeqDF = pd.DataFrame(np.array(wifiSeq2Save), columns=["segid", "coordx", "coordy", "wifiinfos"])
            wifiSeqDF.to_csv(targetFile, encoding="utf-8", index=False)
    elif controlFlag == 1:
        pass

    print("Done.")