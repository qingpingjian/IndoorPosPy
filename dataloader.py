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


def loadWifiScan(filePath, num=15):
    wifiScanDF = pd.read_csv(filePath)
    wifiScanInfo = wifiScanDF.ix[:, ["userid", "coordx", "coordy","wifiinfos"]]
    userID = wifiScanInfo.iloc[0, 0]
    loc = (wifiScanInfo.iloc[0, 1], wifiScanInfo.iloc[0, 2])
    wifiScanDict = {userID: {}}
    pass


def loadRadioMap(filePath):
    radioMapDF = pd.read_csv(filePath)


def loadWifiTest(filePath):
    wifiTestDF = pd.read_csv(filePath)


if __name__ == "__main__":
    print("Done.")