#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/4/20 14:27
@author: Pete
@email: yuwp_1985@163.com
@file: formatdata.py
@software: PyCharm Community Edition
"""
import numpy as np
import os
import pandas as pd
import time

from dataloader import loadWifiScan2

def loadRawData(rawDataDir, C=3, logFlag=False):
    """
    load raw data of Wi-Fi fingerprints and format to np.ndarray
    :param rawDataDir: Wi-Fi raw data parent directory
    :param C: the number Wi-Fi records to form a fp
    :return: Wi-Fi fps dict
    """
    if not os.path.isdir(rawDataDir):
        return None
    wifiFPDict = {} # {userID: [[pos1, pos2], [wifidict1, wifidict2]]}
    fileCounter = 0
    for rt, dirs, files in os.walk(rawDataDir):
        for fileName in files:
            if fileName.endswith("wifi.csv"):
                absolutFilePath = os.path.join(trainFileDir, fileName)
                scanWifiDict = loadWifiScan2(absolutFilePath, num=C)
                for userID in scanWifiDict.keys():
                    if wifiFPDict.has_key(userID):
                        wifiFPDict.get(userID)[0].extend(scanWifiDict.get(userID)[0])
                        wifiFPDict.get(userID)[1].extend(scanWifiDict.get(userID)[1])
                    else:
                        wifiFPDict[userID] = scanWifiDict.get(userID)
                fileCounter += 1
                if logFlag:
                    print("%03d: Loaded the file - %s" % (fileCounter, absolutFilePath))
    return wifiFPDict


def saveDict2File(wifiFPDict, macConfigFileName, wifiRepoFileName, defaultWifi=-100, logFlag=False):

    # wireless access points in all
    apSet = set([])
    for userID in wifiFPDict.keys():
        for wifiDict in wifiFPDict.get(userID)[1]:
            apSet |= set(wifiDict.keys())
    if logFlag:
        print ("Wireless APs Count: %d" % (len(apSet)))
    apList = list(apSet)
    apIDList = ["wap%03d" % (i + 1) for i in range(len(apList))]
    macConfigDF = pd.DataFrame(np.transpose([apList, apIDList]), columns=["mac", "id"])
    macConfigDF.to_csv(macConfigFileName, encoding='utf-8', index=False)
    if logFlag:
        print("Save Wireless APs to %s" % (macConfigFileName))

    # Re-orginaze the Wi-Fi dict
    heading = []
    heading.extend(apIDList)
    heading.extend(["coordx", "coordy", "userid"])
    wifiInfoList = []
    for userID in wifiFPDict.keys():
        locList = wifiFPDict.get(userID)[0]
        wifiDictList = wifiFPDict.get(userID)[1]
        for i in range(len(locList)):
            wifiRecord = []
            wifiDict = wifiDictList[i]
            wifiRecord = [float(np.mean(wifiDict.get(ap))) if wifiDict.has_key(ap) else defaultWifi for ap in apList]
            wifiRecord.extend(locList[i])
            wifiRecord.append(userID)
            wifiInfoList.append(wifiRecord)
    wifiRepoDF = pd.DataFrame(np.array(wifiInfoList), columns=heading)
    wifiRepoDF.to_csv(wifiRepoFileName, encoding='utf-8', index=False)
    if logFlag:
        print("Save Wi-Fi raw data to %s" % (wifiRepoFileName))
    return

if __name__ == "__main__":
    # Format the Wi-Fi raw data to train a predict model
    trainTitle = "wifi_train"
    macConfigTitle = "mac_list"
    dateStr = time.strftime("%Y%m%d", time.localtime())
    wifiRepoFileName = "%s-%s.csv" % (dateStr, trainTitle)
    macConfigFileName = "%s-%s.csv" % (dateStr, macConfigTitle)
    # Process the train data set
    trainFileDir = "../RadioMap"

    wifiTrainDict = loadRawData(trainFileDir, C=5, logFlag=True)
    saveDict2File(wifiTrainDict, macConfigFileName, wifiRepoFileName, logFlag=True)

    print("Done.")