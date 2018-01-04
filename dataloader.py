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
import pandas as pd


def loadAcceData(filePath, relativeTime = True):
    gravity = 9.411869  # Expect value of holding mobile phone static
    acceDF = pd.read_csv(filePath)
    acceInfo = acceDF.ix[:,['Time(s)', 'acce_x', 'acce_y', 'acce_z']]
    acceTimeList = []
    acceValueList = []
    for acceRecord in acceInfo.values:
        acceTimeList.append(acceRecord[0])
        xAxis = acceRecord[1]
        yAxis = acceRecord[2]
        zAxis = acceRecord[3]
        acceValueList.append(math.sqrt(math.pow(xAxis, 2) + math.pow(yAxis, 2) + math.pow(zAxis, 2)) - gravity)
    if relativeTime:
        acceTimeList = [(t - acceTimeList[0]) for t in acceTimeList]
    return acceTimeList, acceValueList


def loadGyroData(filePath, relativeTime = True):
    gyroDF = pd.read_csv(filePath)
    gyroInfo = gyroDF.ix[:, ["Time(s)", "gyro_z"]]
    gyroTimeList = []
    gyroValueList = []
    for gyroRecord in gyroInfo.values:
        gyroTimeList.append(gyroRecord[0])
        gyroValueList.append(gyroRecord[1])
    if relativeTime:
        gyroTimeList = [(t - gyroTimeList[0]) for t in gyroTimeList]
    return gyroTimeList, gyroValueList


def locTransform(orignLoc, moveVector, rotStr):
    """
    Transform the origin location to new coordinate based on moveVector and rotStr
    eg. Transform the global location to coordinate of one experimental path
    :param orignLoc:  location at original coordinate
    :param moveVector:  move vector
    :param rotStr:  rotation angle
    :return: location at new coordinate
    """
    moveLoc = (orignLoc[0] - moveVector[0], orignLoc[1] - moveVector[1])
    x = 0
    y = 0
    if rotStr == "0":
        x = moveLoc[0]
        y = moveLoc[1]
    elif (rotStr == "90"):
        x = - moveLoc[1]
        y = moveLoc[0]
    elif rotStr == "180":
        x = 0.0 - moveLoc[0]
        y = 0.0 - moveLoc[1]
    elif rotStr == "270":
        x = moveLoc[1]
        y = 0.0 - moveLoc[0]
    return (x, y)


def loadRouteData(filePath, transform=True, rotAngle="0"):
    locationDF = pd.read_csv(filePath)
    locationList = [(loc[0], loc[1]) for loc in locationDF.values]
    if transform:
        moveVector = locationList[0]
        locationList = [locTransform(loc, moveVector, rotAngle) for loc in locationList]
    return locationList


def saveLocationError(filePath, errorList):
    with open(filePath, "w") as errorFile:
        for locErr in errorList:
            errorFile.write("%.3f\n" % locErr)
    return


if __name__ == "__main__":
    locationFilePath = "./RawData/SimplePDR/20170702210514_route.txt"
    print(loadRouteData(locationFilePath))
    print("Done.")