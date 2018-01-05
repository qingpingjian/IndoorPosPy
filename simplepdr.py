#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/1/2 10:53
@author: Pete
@email: yuwp_1985@163.com
@file: simplepdr.py
@software: PyCharm Community Edition
"""

import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.ticker import  MultipleLocator, FormatStrFormatter

from comutil import *
from dataloader import loadAcceData, loadGyroData
from stepcounter import SimpleStepCounter


class PDR(object):
    def __init__(self, personID="pete"):
        self.personID = personID
        return

    def getLocEstimation(self, acceTimeList, acceValueList, gyroTimeList, gyroValueList):
        para = modelParameterDict.get(self.personID)
        # Count step
        acceValueArray = butterFilter(acceValueList)
        # Algorithm of step counter
        sc = SimpleStepCounter(para[0], para[1], para[2], para[3])
        allIndexList = sc.countStep(acceTimeList, acceValueArray)
        stIndexList = allIndexList[0::3]
        stTimeList = [acceTimeList[i] for i in stIndexList]
        edIndexList = allIndexList[2::3]
        edTimeList = [acceTimeList[i] for i in edIndexList]
        stepNum = len(stIndexList)

        # Get step length
        stepFreq = stepNum / (edTimeList[-1] - stTimeList[0])
        stepLength = para[4] * stepFreq + para[5]
        print("Step Num is %d, Step Frequency is %.3f and Step Length is %.4f" % (stepNum, stepFreq, stepLength))

        # Get rotation angle
        rotationList = rotationAngle(gyroTimeList, gyroValueList)

        # Estimate locations
        estiLocList = [(0, 0)]
        currentIndex = 0
        for i in range(len(stIndexList)):
            asTime = stTimeList[i]
            aeTime = edTimeList[i]
            # stepLength = para[4] * (1.0 / (aeTime - asTime)) +  para[5]
            rotStartIndex = timeAlign(asTime, gyroTimeList, currentIndex)
            currentIndex = rotStartIndex - 1
            rotEndIndex = timeAlign(aeTime, gyroTimeList, currentIndex)
            currentIndex = rotEndIndex - 1
            direction = meanAngle(rotationList[rotStartIndex:rotEndIndex + 1])
            lastLoc = estiLocList[-1]
            xLoc = lastLoc[0] + stepLength * math.sin(direction)
            yLoc = lastLoc[1] + stepLength * math.cos(direction)
            estiLocList.append((xLoc, yLoc))
        return estiLocList

    def locTransform(self, originLocList, rotStr, moveVector):
        newLocList = []
        for loc in originLocList:
            x = y = 0
            # clockwise rotation first
            if rotStr == "0":
                x = loc[0]
                y = loc[1]
            elif (rotStr == "90"):
                x = - loc[1]
                y = loc[0]
            elif rotStr == "180":
                x = 0.0 - loc[0]
                y = 0.0 - loc[1]
            elif rotStr == "270":
                x = loc[1]
                y = 0.0 - loc[0]
            newLocList.append((moveVector[0] + x, moveVector[1] + y))
        return newLocList


if __name__ == "__main__":
    sensorFilePath = ("./Examples/SimplePDR/20170702210514_acce.txt", "./Examples/SimplePDR/20170702210514_gyro.txt")
    locationFilePath = "./Examples/SimplePDR/20170702210514_route.txt"
    estimationFilePath = "./Examples/SimplePDR/20170702210514_estimate.txt"
    routeRotation = "0"
    moveVector = (0, 0)

    # Load sensor data from files
    acceTimeList, acceValueList = loadAcceData(sensorFilePath[0], relativeTime=False)
    gyroTimeList, gyroValueList = loadGyroData(sensorFilePath[1], relativeTime=False)

    # Get location estimation at global coordination
    myPDR = PDR()
    locEstList = myPDR.getLocEstimation(acceTimeList, acceValueList, gyroTimeList, gyroValueList)
    # From the local route coordinate to global coordinate
    locEstList = myPDR.locTransform(locEstList, routeRotation, moveVector)

    # Save the estimate locations
    locEstList = [(round(loc[0] * 1000) / 1000, round(loc[1] * 1000) / 1000) for loc in locEstList]
    locEstDF = pd.DataFrame(np.array(locEstList), columns=["EX(m)", "EY(m)"])
    locEstDF.to_csv(estimationFilePath, encoding='utf-8', index=False)

    # load real locations
    locRealDF = pd.read_csv(locationFilePath)

    # Calculate the location errors
    locRealList = [(loc[0], loc[1]) for loc in locRealDF.values]
    errorList = distError(locRealList, locEstList)

    # Save the errors
    errorList = [round(err * 1000) / 1000 for err in errorList]
    errorFilePath = "%s_error.txt" % locationFilePath[0:-4]
    errorDF = pd.DataFrame(np.array(errorList), columns=["Error(m)"])
    errorDF.to_csv(errorFilePath, encoding='utf-8', index=False)

    # Show the errors
    pdrxMajorLocator = MultipleLocator(10)
    pdrxMajorFormatter = FormatStrFormatter("%d")
    pdrxMinorLocator = MultipleLocator(5)
    pdryMajorLocator = MultipleLocator(1.0)
    pdryMajorFormatter = FormatStrFormatter("%.1f")
    pdryMinorLocator = MultipleLocator(0.5)

    fig = plt.figure()
    pdrAxe = fig.add_subplot(111)

    pdrAxe.xaxis.set_major_locator(pdrxMajorLocator)
    pdrAxe.xaxis.set_major_formatter(pdrxMajorFormatter)
    pdrAxe.xaxis.set_minor_locator(pdrxMinorLocator)
    pdrAxe.yaxis.set_major_locator(pdryMajorLocator)
    pdrAxe.yaxis.set_major_formatter(pdryMajorFormatter)
    pdrAxe.yaxis.set_minor_locator(pdryMinorLocator)
    pdrAxe.set_xlabel("$Step\ Number$")
    pdrAxe.set_ylabel("$Position\ Error(m)$")
    pdrAxe.plot(range(len(errorList)), errorList, color="r", lw=2, label="PDR")
    plt.legend(loc = 2)
    plt.grid()
    plt.show()

    print("Done.")