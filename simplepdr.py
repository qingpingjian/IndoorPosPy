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
import random as rd
import time

from matplotlib.ticker import  MultipleLocator, FormatStrFormatter

from comutil import *
from dataloader import loadAcceData, loadGyroData
from stepcounter import SimpleStepCounter


class PDR(object):
    def __init__(self, personID="pete"):
        self.personID = personID
        return

    def getLocEstimation(self, acceTimeList, acceValueList, gyroTimeList, gyroValueList, stepError=0, headingError=0):
        para = modelParameterDict.get(self.personID)
        # Count step
        acceValueArray = butterFilter(acceValueList)
        # Algorithm of step counter
        sc = SimpleStepCounter(self.personID)
        allIndexList = sc.countStep(acceTimeList, acceValueArray)
        stIndexList = allIndexList[0::3]
        stTimeList = [acceTimeList[i] for i in stIndexList]
        edIndexList = allIndexList[2::3]
        edTimeList = [acceTimeList[i] for i in edIndexList]
        stepNum = len(stIndexList)

        # Get step length
        stepFreq = stepNum / (edTimeList[-1] - stTimeList[0])
        stepLengthRegress = para[4] * stepFreq + para[5]

        # print("Step Num is %d, Step Frequency is %.3f and Step Length is %.4f" % (stepNum, stepFreq, stepLengthRegress))

        # Get rotation angle
        rotationList = rotationAngle(gyroTimeList, gyroValueList)

        # degree to radian
        headingErrorInRad = headingError * (math.pi / 180.0)

        # Estimate locations
        estiLocList = [(0, 0)]
        currentIndex = 0
        for i in range(len(stIndexList)):
            asTime = stTimeList[i]
            aeTime = edTimeList[i]

            # stepLength = para[4] * (1.0 / (aeTime - asTime)) +  para[5]
            # Step length with gaussian errors
            stepLength = stepLengthRegress + (rd.gauss(0, stepError) if stepError > 0.0001 else 0.0)

            rotStartIndex = timeAlign(asTime, gyroTimeList, currentIndex)
            currentIndex = rotStartIndex - 1
            rotEndIndex = timeAlign(aeTime, gyroTimeList, currentIndex)
            currentIndex = rotEndIndex - 1

            # Heading direction with gaussian errors
            direction = meanAngle(rotationList[rotStartIndex:rotEndIndex + 1])
            deltaHeading = rd.gauss(0, headingErrorInRad) if headingErrorInRad > 0.0000001 else 0.0
            direction = direction + deltaHeading

            lastLoc = estiLocList[-1]
            xLoc = lastLoc[0] + stepLength * math.sin(direction)
            yLoc = lastLoc[1] + stepLength * math.cos(direction)
            estiLocList.append((xLoc, yLoc))
        return estiLocList


if __name__ == "__main__":
    # TODO: *****-- ***** #
    controlFlag = 0 # 0 : Testing Demo, 1 : AiFiMatch
    showFlags = (True, False, False, False)
    myPDR = PDR() # pete by default
    if controlFlag == 0:
        # TODO: Testing Data Demo
        sensorFilePath = ("./Examples/SimplePDR/20170702210514_acce.csv",
                          "./Examples/SimplePDR/20170702210514_gyro.csv")
        locationFilePath = "./Examples/SimplePDR/20170702210514_route.csv"
        estimationFilePath = "./Examples/SimplePDR/20170702210514_estimate.csv"
        routeRotClockWise = "0"
        moveVector = (0, 0)

        # Load sensor data from files
        acceTimeList, acceValueList = loadAcceData(sensorFilePath[0], relativeTime=False)
        gyroTimeList, gyroValueList = loadGyroData(sensorFilePath[1], relativeTime=False)

        # load real locations
        locRealDF = pd.read_csv(locationFilePath)
        locRealList = [(loc[0], loc[1]) for loc in locRealDF.values]

        locEstRelList = myPDR.getLocEstimation(acceTimeList, acceValueList,
                                               gyroTimeList, gyroValueList)
        # From the relative route coordinate to global coordinate
        locEstWorldList = [locTransformR2W(relLoc, moveVector, routeRotClockWise) for relLoc in locEstRelList]
        # Format the estimate locations
        locEstList = [(round(loc[0] * 1000) / 1000, round(loc[1] * 1000) / 1000) for loc in locEstWorldList]

        # Calculate the location errors
        errorList = distError(locRealList, locEstList)

        print("Average Error Distance is %.3f" % (np.mean(errorList)))

        # Show the errors
        if showFlags[controlFlag]:
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
            plt.legend(loc=2)
            plt.grid()
            plt.show()
    elif controlFlag == 1:
        rawDataArray = []
        # initial point and direction
        routeRotClockWise = "0"
        moveVector = (1.2, 1.7)
        # TODO: *****-- ***** #
        saveFlags = (False, False, False) # From 0 index
        rootDirectory = "./RawData/AiFiMatch/ErrorInfluence"
        dataBelongs = "t1"
        # TODO: *****-- ***** #
        trajectorySwitch = 3
        if trajectorySwitch == 1:
            # TODO: First trajectory of AiFiMatch
            rawDataArrayofFirst = [
                # (# The first one
                #     "./RawData/AiFiMatch/FirstTrajectory/20180302213401_acce.csv",
                #     "./RawData/AiFiMatch/FirstTrajectory/20180302213401_gyro.csv",
                #     "./RawData/AiFiMatch/FirstTrajectory/20180302213401_route.csv",
                # ),
                (# The second one(*)
                    "./RawData/AiFiMatch/FirstTrajectory/20180302213910_acce.csv",
                    "./RawData/AiFiMatch/FirstTrajectory/20180302213910_gyro.csv",
                    "./RawData/AiFiMatch/FirstTrajectory/20180302213910_route.csv",
                ),
                (# The third one
                    "./RawData/AiFiMatch/FirstTrajectory/20180302214450_acce.csv",
                    "./RawData/AiFiMatch/FirstTrajectory/20180302214450_gyro.csv",
                    "./RawData/AiFiMatch/FirstTrajectory/20180302214450_route.csv",
                ),
            ]
            # initial point and direction
            firstRouteRotClockWise = "0"
            firstMoveVector = (1.2, 1.7)
            rawDataArray.extend(rawDataArrayofFirst)
            routeRotClockWise = firstRouteRotClockWise
            moveVector = firstMoveVector
            dataBelongs = "t1"
        elif trajectorySwitch == 2:
            # TODO: Second trajectory of AiFiMatch
            rawDataArrayofSecond = [
                (# The second one(*)
                    "./RawData/AiFiMatch/SecondTrajectory/20180303165821_acce.csv",
                    "./RawData/AiFiMatch/SecondTrajectory/20180303165821_gyro.csv",
                    "./RawData/AiFiMatch/SecondTrajectory/20180303165821_route.csv",
                )
            ]
            # initial point and direction
            secondRouteRotClockWise = "0"
            secondMoveVector = (49.800, 59.15)
            rawDataArray.extend(rawDataArrayofSecond)
            routeRotClockWise = secondRouteRotClockWise
            moveVector = secondMoveVector
            dataBelongs = "t2"
            pass
        elif trajectorySwitch == 3:
            # TODO: Third Trajectory of AiFiMatch
            rawDataArrayofThird = [
                (# The fourth one(*)
                    "./RawData/AiFiMatch/ThirdTrajectory/20180303143913_acce.csv",
                    "./RawData/AiFiMatch/ThirdTrajectory/20180303143913_gyro.csv",
                    "./RawData/AiFiMatch/ThirdTrajectory/20180303143913_route.csv",
                )
            ]
            # initial point and direction
            thirdRouteRotClockWise = "0"
            thirdMoveVector = (49.8, 1.95)
            rawDataArray.extend(rawDataArrayofThird)
            routeRotClockWise = thirdRouteRotClockWise
            moveVector = thirdMoveVector
            dataBelongs = "t3"

        # TODO: *****-- ***** #
        # Performance VS. Step Length Error
        stepLengthErrorList = (0.0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5)
        headingErrorList = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        errorType = "step"
        # Performance VS. Heading Error
        stepLengthErrorList = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        headingErrorList = (0, 10, 15, 20, 25, 30, 35, 40, 45, 50)
        errorType = "heading"

        errorListInSensorError = []
        for i in range(min(len(stepLengthErrorList), len(headingErrorList))):
            slError4Test = stepLengthErrorList[i]
            headingError4Test = headingErrorList[i]
            errorBySteps = []
            for k in range(10):
                for j in range(len(rawDataArray)):
                    filePaths = rawDataArray[j]
                    # Load sensor data from files
                    acceTimeList, acceValueList = loadAcceData(filePaths[0], relativeTime=False)
                    gyroTimeList, gyroValueList = loadGyroData(filePaths[1], relativeTime=False)

                    # load real locations
                    locRealDF = pd.read_csv(filePaths[2])
                    locRealList = [(loc[0], loc[1]) for loc in locRealDF.values]
                    locEstRelList = myPDR.getLocEstimation(acceTimeList, acceValueList,
                                                           gyroTimeList, gyroValueList,
                                                           stepError=stepLengthErrorList[i],
                                                           headingError=headingErrorList[i])
                    # From the relative route coordinate to global coordinate
                    locEstWorldList = [locTransformR2W(relLoc, moveVector, routeRotClockWise) for relLoc in locEstRelList]
                    # Format the estimate locations
                    locEstList = [(round(loc[0] * 1000) / 1000, round(loc[1] * 1000) / 1000) for loc in locEstWorldList]
                    # Calculate the location errors
                    errorList = distError(locRealList, locEstList)
                    errorBySteps.append(errorList)
                    # Show the errors
                    if showFlags[controlFlag]:
                        print [round(err * 1000) / 1000 for err in errorList]
            errorAvgInTimes = map(lambda errs: np.mean(errs), zip(*errorBySteps))
            print "Step Error ", slError4Test, " Heading Error ", headingError4Test, " Position Error: ", round(np.mean(errorAvgInTimes) * 1000) / 1000
            errorListInSensorError.append((slError4Test, headingError4Test, round(np.mean(errorAvgInTimes) * 1000) / 1000))
        print errorListInSensorError
        if saveFlags[trajectorySwitch-1]:
            errorFilePath = "%s/pdr_error_%s_%s_%s.csv" % (rootDirectory, errorType, dataBelongs, time.strftime("%m%d"))
            errorDF = pd.DataFrame(np.array(errorListInSensorError), columns=["Delta_Step", "Delta_Heading", "Error(m)"])
            errorDF.to_csv(errorFilePath, encoding='utf-8', index=False)

    print("Done.")