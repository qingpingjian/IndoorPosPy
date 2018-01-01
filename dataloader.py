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
import pandas as pd
import scipy.signal as signal


def butterFilter(data, fs=50, lowcut=0.5, highcut=4.0, order=2):
    """
    Apply butterworth filter to the raw data
    :param data: raw data
    :param fs: sample frequency
    :param lowcut: low frequency threshold
    :param highcut: high frequency threshold
    :param order: butterworth band pass in  order value, 2 by default
    :return: filtered data
    """
    # butter band pass
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    dataArray = np.array(data).astype(np.float)
    y = signal.lfilter(b, a, dataArray)
    return y


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


if __name__ == "__main__":
    print("Done.")