#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/1/1 下午9:04
@author: Pete
@email: yuwp_1985@163.com
@file: dataloader.py
@software: PyCharm Community Edition
"""
import math
import numpy as np
import os
import pandas as pd

from wififunc import wifiStrAnalysis, wifiSequenceProcess

TIMESTAMP_BASELINE = 1490000000000

def loadAcceData(filePath, relativeTime = True):
    gravity = 9.411869  # Expect value of holding mobile phone static
    acceDF = pd.read_csv(filePath)
    acceInfo = acceDF.ix[:,['timestamp', 'acce_x', 'acce_y', 'acce_z']]
    acceTimeList = []
    acceValueList = []
    for acceRecord in acceInfo.values:
        acceTimeList.append((acceRecord[0] - TIMESTAMP_BASELINE)/ 1000.0) # milliseconds to seconds
        xAxis = acceRecord[1]
        yAxis = acceRecord[2]
        zAxis = acceRecord[3]
        acceValueList.append(math.sqrt(math.pow(xAxis, 2) + math.pow(yAxis, 2) + math.pow(zAxis, 2)) - gravity)
    if relativeTime:
        acceTimeList = [(t - acceTimeList[0]) for t in acceTimeList]
    return acceTimeList, acceValueList


def loadGyroData(filePath, relativeTime = True):
    gyroDF = pd.read_csv(filePath)
    gyroInfo = gyroDF.ix[:, ["timestamp", "gyro_z"]]
    gyroTimeList = []
    gyroValueList = []
    for gyroRecord in gyroInfo.values:
        gyroTimeList.append((gyroRecord[0] - TIMESTAMP_BASELINE) / 1000.0) # milliseconds to seconds
        gyroValueList.append(gyroRecord[1])
    if relativeTime:
        gyroTimeList = [(t - gyroTimeList[0]) for t in gyroTimeList]
    return gyroTimeList, gyroValueList


def loadCompData(filePath, relativeTime=True):
    compDF = pd.read_csv(filePath)
    compInfo = compDF.ix[:, ["timestamp", "azimut"]]
    compTimeList = []
    compValueList = []
    for compRecord in compInfo.values:
        compTimeList.append((compRecord[0] - TIMESTAMP_BASELINE) / 1000.0) # milliseconds to seconds
        compValueList.append(-1.0 * compRecord[1])    # There is a minus between compass data and gyroscope data
    if relativeTime:
        compTimeList = [(t - compTimeList[0]) for t in compTimeList]
    return compTimeList, compValueList


def loadMovingWifi(wifiFilePath):
    wifiScanDF = pd.read_csv(wifiFilePath)
    wifiScanInfo = wifiScanDF.ix[:, ["timestamp", "wifiinfos"]]
    wifiTimeList = []
    wifiScanList = []
    for wifiRecord in wifiScanInfo.values:
        wifiTimeList.append((wifiRecord[0] - TIMESTAMP_BASELINE) / 1000.0) # milliseconds to seconds
        wifiScanList.append(wifiRecord[1])
    return wifiTimeList, wifiScanList


def loadWifiScan(filePath, num=15, stat=False):
    wifiScanDF = pd.read_csv(filePath)
    wifiScanInfo = wifiScanDF.ix[:, ["userid", "coordx", "coordy", "wifiinfos"]]
    userID = wifiScanInfo.iloc[0, 0]
    loc = (wifiScanInfo.iloc[0, 1], wifiScanInfo.iloc[0, 2])
    wifiScanDict = {userID: [[], [], []]}
    count = int(math.ceil((1.0 * wifiScanInfo.shape[0]) / num))
    for i in range(count):
        wifiScanDict.get(userID)[0].append(loc)
        wifiDict = wifiStrAnalysis(wifiScanInfo.ix[0 + i * num : 15 + i * num, "wifiinfos"].values)
        wifiScanDict.get(userID)[1].append(wifiDict)
        if stat:
            wifiStatDict = {}
            for wifi in wifiDict.keys():
                rssList = wifiDict.get(wifi)
                # std VS 3.0: Optimal calculation for bayes algorithm according to noise
                wifiStatDict[wifi] = (np.mean(rssList), np.max((np.std(rssList), 3.0)))
            wifiScanDict.get(userID)[2].append(wifiStatDict)
    return wifiScanDict


def loadRadioMap(trainFileDir, statFlag=False):
    if not os.path.isdir(trainFileDir):
        return None
    radioMapDict = {}
    for rt, dirs, files in os.walk(trainFileDir):
        for fileName in files:
            if fileName.endswith("wifi.csv"):
                scanWifiDict = loadWifiScan(os.path.join(trainFileDir, fileName), num=15, stat=statFlag)
                for userID in scanWifiDict.keys():
                    if radioMapDict.has_key(userID):
                        radioMapDict.get(userID)[0].extend(scanWifiDict.get(userID)[0])
                        radioMapDict.get(userID)[1].extend(scanWifiDict.get(userID)[1])
                        if statFlag:
                            radioMapDict.get(userID)[2].extend(scanWifiDict.get(userID)[2])
                    else:
                        radioMapDict[userID] = scanWifiDict.get(userID)
    return radioMapDict


def loadWifiTest(testFileDir):
    if not os.path.isdir(testFileDir):
        return None
    wifiTestDict = {}
    for rt, dirs, files in os.walk(testFileDir):
        for fileName in files:
            if fileName.endswith("wifi.csv"):
                scanWifiDict = loadWifiScan(os.path.join(testFileDir, fileName), num=10)
                for userID in scanWifiDict.keys():
                    if wifiTestDict.has_key(userID):
                        wifiTestDict.get(userID)[0].extend(scanWifiDict.get(userID)[0])
                        wifiTestDict.get(userID)[1].extend(scanWifiDict.get(userID)[1])
                    else:
                        wifiTestDict[userID] = scanWifiDict.get(userID)
    return wifiTestDict


def loadBoundWifi(filePath):
    fingerprintDF = pd.read_csv(filePath)
    fingerprintInfo = fingerprintDF.ix[:,["segid", "coordx", "coordy", "wifiinfos"]]
    segWifiDict = {}
    for fp in fingerprintInfo.values:
        segID = fp[0]
        locX = fp[1]
        locY = fp[2]
        wifiInfo = fp[3]
        if segWifiDict.has_key(segID):
            segWifiDict.get(segID).append((locX, locY, wifiStrAnalysis([wifiInfo])))
        else:
            segWifiDict[segID] = [(locX, locY, wifiStrAnalysis([wifiInfo]))]
    return segWifiDict

def loadCrowdSourcedWifi(wifiBoundDir):
    if not os.path.isdir(wifiBoundDir):
        return None
    radioMapDict = {} # {segID:[(x1, y1, wifidict), (x2, y2, wifidict2)]}
    for rt, dirs, files in os.walk(wifiBoundDir):
        for fileName in files:
            if fileName.endswith("bind.csv"):
                segWifiDict = loadBoundWifi(os.path.join(wifiBoundDir, fileName))
                for segID, fp in segWifiDict.iteritems():
                    if radioMapDict.has_key(segID):
                        radioMapDict.get(segID).extend(fp)
                    else:
                        radioMapDict[segID] = fp
    # preprocess the bound wifi fingerprints
    processedRadioMapDict = {}
    for segID, fp in radioMapDict.iteritems():
        processedRadioMapDict[segID] = wifiSequenceProcess(fp)
    print processedRadioMapDict.keys()
    return processedRadioMapDict


if __name__ == "__main__":
    # wifiScanFilePath = "./RawData/RadioMap/20180104202838_wifi.csv"
    # print (loadWifiScan(wifiScanFilePath))
    wifiBoundDir = "./RawData/AiFiMatch/SegmentFingerprint/"
    loadCrowdSourcedWifi(wifiBoundDir)
    print("Done.")