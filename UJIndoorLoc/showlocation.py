#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/4/26 20:02
@author: Pete
@email: yuwp_1985@163.com
@file: showlocation.py
@software: PyCharm Community Edition
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

def spaceSave(wifiFingerprintFile):
    headings = ["BUILDINGID", "FLOOR", "SPACEID"]
    newHeadings = ["FLOORCODE", "SPACEID"]
    wifiDF = pd.read_csv(wifiFingerprintFile)
    spaceArray = wifiDF.ix[:, headings].values.astype(np.int32)
    spaceDF = pd.DataFrame(np.column_stack((spaceArray[:,0] * 10 + spaceArray[:,1], spaceArray[:,2])), columns=newHeadings)
    spaceDF.to_csv("trainingSpace.csv", encoding='utf-8', index=False)
    return

def showLoc(wifiFingerprintFile, debugFlag=False):
    headings = ["LONGITUDE", "LATITUDE", "BUILDINGID", "FLOOR", "SPACEID"]
    wifiDF = pd.read_csv(wifiFingerprintFile)
    if debugFlag:
        wifiDF = wifiDF.head(2000)
    locArray = wifiDF.ix[:,headings].values
    coordArray = locArray[:,0:2]
    locDict = {}
    for locInfo in locArray:
        floorCoder = "%d-%d" % (locInfo[2], locInfo[3])
        if locDict.has_key(floorCoder):
            locDict.get(floorCoder).append((locInfo[0], locInfo[1]))
        else:
            locDict[floorCoder] = [(locInfo[0], locInfo[1])]

    floorCoderList = locDict.keys()
    np.random.seed(np.floor(time.time()).astype(np.int32))
    floorNum = np.random.randint(0, len(floorCoderList))
    fc =  floorCoderList[floorNum]
    fc = "2-4"
    floorLocArray = np.array(locDict.get(fc))

    minValues = np.min(floorLocArray, axis=0)
    print minValues
    maxValues = np.max(floorLocArray, axis=0)
    print maxValues
    maxDist = np.sqrt(np.sum((maxValues - minValues)**2))
    print type(maxValues), maxDist

    print floorLocArray[:,0].shape, floorLocArray[:,1].shape
    # Show the locations in this floor
    fig = plt.figure()
    locAxe = fig.add_subplot(111)
    locAxe.set_xlabel("Longitude")
    locAxe.set_ylabel("Latitude")
    locAxe.scatter(floorLocArray[:,0], floorLocArray[:,1], marker="o", c="red")
    plt.show()
    return

def showLoc2(wifiFingerprintFile, debugFlag=False):
    headings = ["BUILDINGID", "FLOOR", "SPACEID"]
    wifiDF = pd.read_csv(wifiFingerprintFile)
    if debugFlag:
        wifiDF = wifiDF.head(200)
    spaceArray = wifiDF.ix[:,headings].values
    spaceIDDict = {}
    spaceDict2 = {}
    for spaceRecord in spaceArray:
        buildID = spaceRecord[0]
        if spaceIDDict.has_key(buildID):
            spaceIDDict[buildID].append((buildID + 1) * 10000 + (spaceRecord[1] + 1) * 1000 + spaceRecord[2])
            spaceDict2[buildID].append((spaceRecord[1] + 1) * 1000 + spaceRecord[2])
        else:
            spaceIDDict[buildID] = [(buildID + 1) * 10000 + (spaceRecord[1] + 1) * 1000 + spaceRecord[2]]
            spaceDict2[buildID] = [(spaceRecord[1] + 1) * 1000 + spaceRecord[2]]
    buildIDList = spaceIDDict.keys()
    print len(spaceIDDict[buildIDList[2]])
    print len(sorted(set(spaceDict2[buildIDList[2]])))
    print len(set(spaceIDDict[buildIDList[2]]))
    return


if __name__ == "__main__":
    wifiTrainFile = "trainingData.csv"
    #spaceSave(wifiTrainFile)
    showLoc(wifiTrainFile, debugFlag=True)
    # showLoc2(wifiTrainFile, debugFlag=False)
    print("Done.")