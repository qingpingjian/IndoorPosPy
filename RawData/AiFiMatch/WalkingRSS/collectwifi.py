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
import time

from comutil import *
from dataloader import loadAcceData, loadMovingWifi
from stepcounter import SimpleStepCounter
from wififunc import wifiDict2Str, wifiSequenceProcess, wifiSeqJaccardDist

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
    saveFlags = (True, True, True, True)
    controlFlag = 2
    if controlFlag == 0: # 0 : tra01 & 360n5 & radiomap
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
        if saveFlags[controlFlag]:
            wifiSeq2Save = [("tra01", round(wifi[0] * 1000) / 1000, round(wifi[1] * 1000) / 1000, wifiDict2Str(wifi[2])) for wifi in wifiSequence]
            wifiSeqDF = pd.DataFrame(np.array(wifiSeq2Save), columns=["segid", "coordx", "coordy", "wifiinfos"])
            wifiSeqDF.to_csv(targetFile, encoding="utf-8", index=False)
    elif controlFlag == 1: # 1 : tra01 & 360n5 & testing
        radiomapFile = "20180508163535_wifi_crowd.csv"
        testingFilesArray = (
            # Direction One
            "20180509165157_wifi.csv",
            "20180509165354_wifi.csv",
            "20180509165638_wifi.csv",
            # Direction Two
            "20180509165247_wifi.csv",
            "20180509165457_wifi.csv",
            "20180509165726_wifi.csv",
        )
        _, baseWifiSeq = loadMovingWifi(radiomapFile, strAnalysis=True)
        # baseWifiSeq = baseWifiSeq[-1::-1]
        jcdDistArray = []
        for testingFile in testingFilesArray:
            _, testingWifiSeq = loadMovingWifi(testingFile, strAnalysis=True)
            if len(testingWifiSeq) < 3:
                print "Do not have enough wifi scan results in this trajectory"
                continue
            jcdTempList = []
            for lenSeq in range(3, len(testingWifiSeq)):
                sameJcd = wifiSeqJaccardDist(baseWifiSeq, testingWifiSeq[0:lenSeq])
                jcdTempList.append((lenSeq, sameJcd))
            print jcdTempList
            jcdLen = len(jcdDistArray)
            for i in range(len(jcdTempList)):
                if i < jcdLen:
                    jcdDistArray[i][1].append(jcdTempList[i][1])
                else:
                    jcdDistArray.append((jcdTempList[i][0], [jcdTempList[i][1]]))
        print jcdDistArray
        jcdDistList = [(dist[0], float(np.max(dist[1])), float(np.min(dist[1]))) for dist in jcdDistArray]

        if saveFlags[controlFlag]:
            jcdResultFile = "20180509165726_wifi_jaccard_same_360n5_%s.csv" % (time.strftime("%m%d"))
            jcdDistList = [(int(dist[0]), round(dist[1] * 1000) / 1000, round(dist[2] * 1000) / 1000) for dist in jcdDistList]
            jcdResultDF = pd.DataFrame(np.array(jcdDistList), columns=["Count", "Dist(max)", "Dist(min)"])
            jcdResultDF.to_csv(jcdResultFile, encoding='utf-8', index=False)
    elif controlFlag == 2:  # 2 : tra01-sym & 360n5 & testing
        radiomapFile = "20180508163535_wifi_crowd.csv"
        testingFilesArray = (
            # Direction One
            "20180509220215_wifi.csv",
            "20180509220406_wifi.csv",
            "20180509220556_wifi.csv",
            "20180509220725_wifi.csv",
            # Direction Two
            "20180509220301_wifi.csv",
            "20180509220453_wifi.csv",
            "20180509220640_wifi.csv",
            "20180509220813_wifi.csv",
        )
        _, baseWifiSeq = loadMovingWifi(radiomapFile, strAnalysis=True)
        # baseWifiSeq = baseWifiSeq[-1::-1]
        jcdDistArray = []
        for testingFile in testingFilesArray:
            _, testingWifiSeq = loadMovingWifi(testingFile, strAnalysis=True)
            if len(testingWifiSeq) < 3:
                print "Do not have enough wifi scan results in this trajectory"
                continue
            jcdTempList = []
            for lenSeq in range(3, len(testingWifiSeq)):
                sameJcd = wifiSeqJaccardDist(baseWifiSeq, testingWifiSeq[0:lenSeq])
                jcdTempList.append((lenSeq, sameJcd))
            print jcdTempList
            jcdLen = len(jcdDistArray)
            for i in range(len(jcdTempList)):
                if i < jcdLen:
                    jcdDistArray[i][1].append(jcdTempList[i][1])
                else:
                    jcdDistArray.append((jcdTempList[i][0], [jcdTempList[i][1]]))
        print jcdDistArray
        jcdDistList = [(dist[0], float(np.max(dist[1])), float(np.min(dist[1]))) for dist in jcdDistArray]

        if saveFlags[controlFlag]:
            jcdResultFile = "20180509220813_wifi_jaccard_diff_360n5_%s.csv" % (time.strftime("%m%d"))
            jcdDistList = [(int(dist[0]), round(dist[1] * 1000) / 1000, round(dist[2] * 1000) / 1000) for dist in
                           jcdDistList]
            jcdResultDF = pd.DataFrame(np.array(jcdDistList), columns=["Count", "Dist(max)", "Dist(min)"])
            jcdResultDF.to_csv(jcdResultFile, encoding='utf-8', index=False)
    elif controlFlag == 3: # 3: tra01 & coolpad & testing
        radiomapFile = "20180508163535_wifi_crowd.csv"
        testingFilesArray = (
            # Direction One
            "20180509195812_wifi.csv",
            "20180509200006_wifi.csv",
            "20180509200136_wifi.csv",
            # Direction Two
            "20180509195857_wifi.csv",
            "20180509200050_wifi.csv",
            "20180509200222_wifi.csv",
        )
        _, baseWifiSeq = loadMovingWifi(radiomapFile, strAnalysis=True)
        # baseWifiSeq = baseWifiSeq[-1::-1]
        jcdDistArray = []
        for testingFile in testingFilesArray:
            _, testingWifiSeq = loadMovingWifi(testingFile, strAnalysis=True)
            if len(testingWifiSeq) < 3:
                print "Do not have enough wifi scan results in this trajectory"
                continue
            jcdTempList = []
            for lenSeq in range(3, len(testingWifiSeq)):
                sameJcd = wifiSeqJaccardDist(baseWifiSeq, testingWifiSeq[0:lenSeq])
                jcdTempList.append((lenSeq, sameJcd))
            print jcdTempList
            jcdLen = len(jcdDistArray)
            for i in range(len(jcdTempList)):
                if i < jcdLen:
                    jcdDistArray[i][1].append(jcdTempList[i][1])
                else:
                    jcdDistArray.append((jcdTempList[i][0], [jcdTempList[i][1]]))
        print jcdDistArray
        jcdDistList = [(dist[0], float(np.max(dist[1])), float(np.min(dist[1]))) for dist in jcdDistArray]


        if saveFlags[controlFlag]:
            jcdResultFile = "20180509200222_wifi_jaccard_same_coolpad_%s.csv" % (time.strftime("%m%d"))
            jcdDistList = [(int(dist[0]), round(dist[1] * 1000) / 1000, round(dist[2] * 1000) / 1000) for dist in
                           jcdDistList]
            jcdResultDF = pd.DataFrame(np.array(jcdDistList), columns=["Count", "Dist(max)", "Dist(min)"])
            jcdResultDF.to_csv(jcdResultFile, encoding='utf-8', index=False)


    print("Done.")