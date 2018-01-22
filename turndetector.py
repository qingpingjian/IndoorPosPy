#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/1/22 15:56
@author: Pete
@email: yuwp_1985@163.com
@file: turndetector.py
@software: PyCharm Community Edition
"""

import matplotlib.pyplot as plt

from comutil import *
from dataloader import loadGyroData

class SimpleTurnDetector(object):

    def __init__(self):
        pass

    def turnPoint(self, timeList, valueList):
        pass

    def detectTurn(self, timeList, valueList):

        pass

if __name__ == "__main__":
    sensorFilePath = ("./Examples/ActivityDetector/20170702210514_acce.csv",
                      "./Examples/ActivityDetector/20170702210514_gyro.csv")
    gyroTimeList, gyroValueList = loadGyroData(sensorFilePath[1])
    rotaValueList = rotationAngle(gyroTimeList, gyroValueList, normalize=False)

    windowSize = 23
    gyroTimeList, gyroValueList = slidingWindowFilter(gyroTimeList, gyroValueList, windowSize)

    # Plot the figures
    fig = plt.figure()
    gyroRateAxes = fig.add_subplot(111)
    rotaAngleAxes = gyroRateAxes.twinx()

    gyroRateAxes.set_xlabel("$Time(s)$")
    gyroRateAxes.set_ylabel("$Rotation Rate(radian/s)$")
    # gyroRateAxes.set_xticklabels(np.array(np.linspace(0, 30, 7), np.int))
    # gyroRateAxes.set_yticklabels(np.linspace(-1.5, 1.5, 7))
    ratePlot, = gyroRateAxes.plot(gyroTimeList, gyroValueList, color="g", label="Rotation Rate")
    # gyroRateAxes.yaxis.label.set_color(ratePlot.get_color())

    rotaAngleAxes.set_ylabel("$Rotation(degree)$")
    # rotaAngleAxes.set_yticklabels(np.array(np.linspace(-100, 20, 7), np.int))
    anglePlot, = rotaAngleAxes.plot(gyroTimeList, [r * 180.0 / math.pi for r in rotaValueList], color="b", linestyle="--", label="Rotation Angle")
    # rotaAngleAxes.yaxis.label.set_color(anglePlot.get_color())

    plt.legend(handles=[ratePlot, anglePlot], loc=4)
    plt.show()

    print("Done.")