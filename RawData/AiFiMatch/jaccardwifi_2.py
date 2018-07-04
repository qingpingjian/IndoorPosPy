#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/3/15 下午11:43
@author: Pete
@email: yuwp_1985@163.com
@file: jaccardwifi.py
@software: PyCharm Community Edition
"""
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import time
from matplotlib.ticker import  MultipleLocator, FormatStrFormatter

from comutil import *
from dataloader import loadAcceData, loadGyroData, loadMovingWifi, loadCrowdSourcedWifi
from stepcounter import SimpleStepCounter
from turndetector import SimpleTurnDetector
from wififunc import wifiSeqJaccardDist

matplotlib.rcParams['font.size'] = 20

def calculateJcdDist(acceTimeList, acceValueList,
                     gyroTimeList, gyroValueList,
                     wifiTimeList, wifiScanList,
                     radioMapDict, personID="pete"):
    # Count step
    acceValueArray = butterFilter(acceValueList)
    # Algorithm of step counter
    sc = SimpleStepCounter(personID)
    allIndexList = sc.countStep(acceTimeList, acceValueArray)
    stIndexList = allIndexList[0::3]
    stTimeList = [acceTimeList[i] for i in stIndexList]
    peakIndexList = allIndexList[1::3]
    peakTimeList = [acceTimeList[i] for i in peakIndexList]
    edIndexList = allIndexList[2::3]
    edTimeList = [acceTimeList[i] for i in edIndexList]
    stepNum = len(stIndexList)
    # Get step length
    para = modelParameterDict.get(personID)
    stepFreq = stepNum / (edTimeList[-1] - stTimeList[0])
    stepLength = para[4] * stepFreq + para[5]
    print("Step Num is %d, Step Frequency is %.3f and Step Length is %.4f" % (stepNum, stepFreq, stepLength))

    # Detect Turns
    rotaValueList = rotationAngle(gyroTimeList, gyroValueList, normalize=False)
    rotaDegreeList = [r * 180.0 / math.pi for r in rotaValueList]
    windowSize = 23
    gyroTimeList, gyroValueList = slidingWindowFilter(gyroTimeList, gyroValueList, windowSize)
    simpleTd = SimpleTurnDetector(personID)
    turnIndexList, rtDegreeIndexList = simpleTd.detectTurn(gyroTimeList, gyroValueList, rotaDegreeList)
    turnStartIndexList = rtDegreeIndexList[0::2]
    turnStartTimeList = [gyroTimeList[i] for i in turnStartIndexList]
    turnTimeList = [gyroTimeList[i] for i in turnIndexList]
    turnEndIndexList = rtDegreeIndexList[1::2]
    turnEndTimeList = [gyroTimeList[i] for i in turnEndIndexList]
    # Turn Type Detected
    turnTypeList = []
    turnStartValueList = [rotaDegreeList[i] for i in turnStartIndexList]
    turnEndValueList = [rotaDegreeList[i] for i in turnEndIndexList]
    for i in range(0, len(turnStartIndexList)):
        turnTypeList.append(simpleTd.turnTranslate(turnEndValueList[i] - turnStartValueList[i], humanFlag=False))
    print "The Turn Detected Results are as follows:", turnTypeList

    # Turn and Step alignment
    tsIndexList, stsIndexList, etsIndexList = turnAlignStep(edTimeList, turnStartTimeList,
                                                            turnTimeList, turnEndTimeList)
    jcdDistList = [] # [(wifi sequence length, jaccard distance value)]
    currentWifiIndex = 0
    for i in range(0, len(turnTypeList) - 1):
        if turnTypeList[i] < 3 and turnTypeList[i + 1] < 3:
            print("%d turn and %d next turn is satisfied" % (i, i + 1))
            walkWifiSeq = []
            # extract wifi sequence from the following step after current turn to the previous step before next turn
            stepStartIndex = tsIndexList[i] + 1
            stepEndIndex = tsIndexList[i+1] - 1
            for j in range(stepStartIndex, stepEndIndex+1):
                # From the current peak timestamp to next peak timestamp
                startWifiTime = peakTimeList[j]
                endWifiTime = peakTimeList[j + 1]
                currentWifiIndex, currentWifiDict = wifiExtract(startWifiTime, endWifiTime, wifiTimeList, wifiScanList,
                                                                currentWifiIndex)
                if currentWifiDict == None:
                    continue
                walkWifiSeq.append(currentWifiDict)
                wifiSegLen = len(walkWifiSeq)
                if wifiSegLen < 3:
                    continue
                segJcd = []
                for segID, fpSeq in radioMapDict.iteritems():
                    fpWifiSeq = [wifiFP[2] for wifiFP in fpSeq]
                    dist = wifiSeqJaccardDist(fpWifiSeq, walkWifiSeq)
                    segJcd.append(dist)
                jcdDistList.append((wifiSegLen, float(np.min(segJcd))))
                print(jcdDistList)
    return jcdDistList

if __name__ == "__main__":
    # Save flags
    saveFlag = True
    # Running Control Flag, 0: Second Trajectory; 1: Third Trajectory; 2: Show Comparison
    controlFlag = 2
    # Load radio map organized by segment
    wifiBoundDir = "./SegmentFingerprint/"
    radioMapDict = loadCrowdSourcedWifi(wifiBoundDir)
    if controlFlag == 0: # Second Trajectory of AiFiMatch
        # TODO: Second Trajectory of AiFiMatch
        sensorFilePathGroup = (
            ("./SecondTrajectory/20180303165540_acce.csv",
            "./SecondTrajectory/20180303165540_gyro.csv",
            "./SecondTrajectory/20180303165540_wifi.csv"),

            ("./SecondTrajectory/20180303165821_acce.csv",
            "./SecondTrajectory/20180303165821_gyro.csv",
            "./SecondTrajectory/20180303165821_wifi.csv"),

            ("./SecondTrajectory/20180303170055_acce.csv",
            "./SecondTrajectory/20180303170055_gyro.csv",
            "./SecondTrajectory/20180303170055_wifi.csv")
            )
        jcdDiffSegList = []
        for sensorFilePath in sensorFilePathGroup:
            acceTimeList, acceValueList = loadAcceData(sensorFilePath[0], relativeTime=False)
            gyroTimeList, gyroValueList = loadGyroData(sensorFilePath[1], relativeTime=False)
            wifiTimeList, wifiScanList = loadMovingWifi(sensorFilePath[2])

            # Calculate the wifi sequence distance based on Jaccard Distance definition
            jcdDistList = calculateJcdDist(acceTimeList, acceValueList, gyroTimeList, gyroValueList,
                             wifiTimeList, wifiScanList, radioMapDict)
            if len(jcdDiffSegList) == 0:
                jcdDiffSegList.extend(jcdDistList)
            else:
                for i in range(len(jcdDiffSegList)):
                    jcdDiffSegList[i] = min(jcdDistList[i], jcdDiffSegList[i]) if i < len(jcdDistList) else jcdDiffSegList[i]

            jcdDistList = [(int(dist[0]), round(dist[1] * 1000) / 1000) for dist in jcdDistList]
            print jcdDistList
        print jcdDiffSegList
        # Process results
        if saveFlag:
            jcdDiffSegFilePath = "jaccard_wifi_diff_segment_%s.csv" % (time.strftime("%m%d"))
            jcdDiffSegList = [(int(dist[0]), round(dist[1] * 1000) / 1000) for dist in jcdDiffSegList]
            jcdDiffSegDF = pd.DataFrame(np.array(jcdDiffSegList), columns=["Count", "Dist"])
            jcdDiffSegDF.to_csv(jcdDiffSegFilePath, encoding='utf-8', index=False)
    elif controlFlag == 1:
        # TODO: Third Trajectory of AiFiMatch
        sensorFilePathGroup = (
            ("./ThirdTrajectory/20180303142423_acce.csv",
            "./ThirdTrajectory/20180303142423_gyro.csv",
            "./ThirdTrajectory/20180303142423_wifi.csv"),

            ("./ThirdTrajectory/20180303143213_acce.csv",
            "./ThirdTrajectory/20180303143213_gyro.csv",
            "./ThirdTrajectory/20180303143213_wifi.csv"),

            ("./ThirdTrajectory/20180303143540_acce.csv",
             "./ThirdTrajectory/20180303143540_gyro.csv",
             "./ThirdTrajectory/20180303143540_wifi.csv"),

            ("./ThirdTrajectory/20180303143913_acce.csv",
            "./ThirdTrajectory/20180303143913_gyro.csv",
            "./ThirdTrajectory/20180303143913_wifi.csv")
            )
        jcdSameSegList = []
        for sensorFilePath in sensorFilePathGroup:
            acceTimeList, acceValueList = loadAcceData(sensorFilePath[0], relativeTime=False)
            gyroTimeList, gyroValueList = loadGyroData(sensorFilePath[1], relativeTime=False)
            wifiTimeList, wifiScanList = loadMovingWifi(sensorFilePath[2])

            # Calculate the wifi sequence distance based on Jaccard Distance definition
            jcdDistList = calculateJcdDist(acceTimeList, acceValueList, gyroTimeList, gyroValueList,
                             wifiTimeList, wifiScanList, radioMapDict)
            if len(jcdSameSegList) == 0:
                jcdSameSegList.extend(jcdDistList)
            else:
                for i in range(len(jcdSameSegList)):
                    jcdSameSegList[i] = min(jcdDistList[i], jcdSameSegList[i]) if i < len(jcdDistList) else jcdSameSegList[i]

            jcdDistList = [(int(dist[0]), round(dist[1] * 1000) / 1000) for dist in jcdDistList]
            print jcdDistList
        print jcdSameSegList
        # Process results
        jcdSameSegList = [(int(dist[0]), dist[1]) for dist in jcdSameSegList]
        jcdSameSegDict = {}
        for jcdSameSeg in jcdSameSegList:
            if jcdSameSegDict.has_key(jcdSameSeg[0]):
                jcdSameSegDict.get(jcdSameSeg[0]).append(jcdSameSeg[1])
            else:
                jcdSameSegDict[jcdSameSeg[0]] = [jcdSameSeg[1]]
        jcdSameSegList = []
        for count, dist in jcdSameSegDict.iteritems():
            jcdSameSegList.append((count, float(np.mean(dist))))
        jcdSameSegList = [(int(dist[0]), round(dist[1] * 1000) / 1000) for dist in jcdSameSegList]
        if saveFlag:
            jcdSameSegFilePath = "jaccard_wifi_same_segment_%s.csv" % (time.strftime("%m%d"))
            jcdSameSegDF = pd.DataFrame(np.array(jcdSameSegList), columns=["Count", "Dist"])
            jcdSameSegDF.to_csv(jcdSameSegFilePath, encoding='utf-8', index=False)
    else:
        jaccardDiffFilePath = "jaccard_wifi_diff_segment_0319.csv"
        jaccardSameFilePath = "jaccard_wifi_same_segment_0319.csv"
        # load experimental results
        countList = range(3, 21)
        jcdDiffDF = pd.read_csv(jaccardDiffFilePath)
        jcdDiffArray = jcdDiffDF.values
        jcdDiffList = [jcd[1] for jcd in jcdDiffArray]
        jcdDiffList = jcdDiffList[0:len(countList)]
        jcdSameDF = pd.read_csv(jaccardSameFilePath)
        jcdSameArray = jcdSameDF.values
        jcdSameList = [jcd[1] for jcd in jcdSameArray]
        jcdSameList = jcdSameList[0:len(countList)]

        # Plot the figures
        fig = plt.figure()
        jcdDistAxes = fig.add_subplot(111)
        jcdDistAxes.set_xlabel("$Length\ of\ WiFi\ Sequence$")
        jcdDistAxes.set_ylabel("$Similarity$")
        oneYMajorLocator = MultipleLocator(0.1)
        oneYMajorFormatter = FormatStrFormatter("%.1f")
        oneYMinorLocator = MultipleLocator(0.05)
        oneXMajorLocator = MultipleLocator(4)
        oneXMajorFormatter = FormatStrFormatter("%d")
        oneXMinorLocator = MultipleLocator(2)
        jcdDistAxes.yaxis.set_major_locator(oneYMajorLocator)
        jcdDistAxes.yaxis.set_major_formatter(oneYMajorFormatter)
        jcdDistAxes.yaxis.set_minor_locator(oneYMinorLocator)
        jcdDistAxes.xaxis.set_major_locator(oneXMajorLocator)
        jcdDistAxes.xaxis.set_major_formatter(oneXMajorFormatter)
        jcdDistAxes.xaxis.set_minor_locator(oneXMinorLocator)
        # jcdDiffPlot, = jcdDistAxes.plot(countList, jcdDiffList, color="b", linestyle="--", marker="o",
        #                                 label="Different Segments")
        jcdDiffPlot, = jcdDistAxes.plot(countList, jcdDiffList, color="b", linestyle="--", marker="s", label="Different Segments")
        jcdSamePlot, = jcdDistAxes.plot(countList, jcdSameList, color="r", marker="o", label="Same Segments")
        #jcdDistAxes.axvline(t, ls=":", lw=2, color="#FF00CC") 0.63
        jcdDistAxes.axhline(0.63, ls=":", lw=2, color="#FF00CC")
        jcdDistAxes.text(11, 0.65, "d=0.63")
        plt.legend(handles=[jcdDiffPlot, jcdSamePlot], loc="best")
        plt.grid(False)
        plt.show()
        pass
    print("Done.")