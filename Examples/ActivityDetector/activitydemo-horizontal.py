#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/1/20 21:27
@author: Pete
@email: yuwp_1985@163.com
@file: activitydemo.py
@software: PyCharm Community Edition
"""
import matplotlib
import matplotlib.pyplot as plt

from matplotlib.ticker import  MultipleLocator, FormatStrFormatter
from comutil import *
from dataloader import loadAcceData, loadGyroData

# Environment Configuration
matplotlib.rcParams['font.size'] = 18

if __name__ == "__main__":
    sensorFilePath = ("20170622153925_acce.csv",
                      "20170622153925_gyro.csv")

    # Load accelerometer data from files
    acceTimeList, acceValueList = loadAcceData(sensorFilePath[0])
    windowSize = 7
    acceVotList, acceVarList = varOfAcce(acceTimeList, acceValueList, windowSize)

    # Stationary
    timeListForStat = acceVotList[51:341]
    timeListForStat = [t - timeListForStat[0] for t in timeListForStat]
    valueListForStat = acceVarList[51:341]

    # Walking
    timeListForWalk = acceVotList[1511:1801]
    timeListForWalk = [t - timeListForWalk[0] for t in timeListForWalk]
    valueListForWalk = acceVarList[1511:1801]

    gyroTimeList, gyroValueList = loadGyroData(sensorFilePath[1])
    windowSize = 21
    gyroTimeFltList, gyroValueFltList = slidingWindowFilter(gyroTimeList, gyroValueList, windowSize)

    # Normal Walking
    timeListForNW = gyroTimeFltList[1101:1601]
    timeListForNW = [t - timeListForNW[0] for t in timeListForNW]
    valueListForNW = gyroValueFltList[1101:1601]

    # Turns
    timeListForTurns = gyroTimeFltList[2581:3081]
    timeListForTurns = [t - timeListForTurns[0] for t in timeListForTurns]
    valueListForTurns = gyroValueFltList[2581:3081]

    # Right and Left turn
    timeListForLeft = gyroTimeList[1781:2281]
    gyroListForLeft = gyroValueList[1781:2281]
    timeListForLeft = [t - timeListForLeft[0] for t in timeListForLeft]
    rotAngleListForLeft = rotationAngle(timeListForLeft, gyroListForLeft, normalize=False)
    rotDegreeListForLeft = [r * 180.0 / math.pi for r in rotAngleListForLeft]

    # Turn around
    timeListForUTurn = gyroTimeList[2581:3081]
    gyroListForUTurn = gyroValueList[2581:3081]
    timeListForUTurn = [t - timeListForUTurn[0] for t in timeListForUTurn]
    rotAngleListForUTurn = rotationAngle(timeListForUTurn, gyroListForUTurn, normalize=False)
    rotDegreeListForUTurn = [r * -180.0 / math.pi for r in rotAngleListForUTurn]

    fig = plt.figure()

    turnSeparateAxe = fig.add_subplot(131)
    turnSeparateAxe.set_ylim(-50, 200)
    turnSeparateAxe.yaxis.set_major_locator(MultipleLocator(50))
    turnSeparateAxe.yaxis.set_major_formatter(FormatStrFormatter("%d"))
    turnSeparateAxe.yaxis.set_minor_locator(MultipleLocator(25))
    turnSeparateAxe.set_xticks([]) # Hidden the x ticks
    turnSeparateAxe.set_ylabel("$Rot. Ang.$")
    # For the publication of a paper version (Just white or black)
    # turnSeparateAxe.plot(timeListForLeft, rotDegreeListForLeft, color="black", lw=4, linestyle="--", label="$Left\ Turn$")
    # turnSeparateAxe.plot(timeListForUTurn, rotDegreeListForUTurn, color="black", lw=2, linestyle="-", label="$U-Turn$")
    turnSeparateAxe.plot(timeListForLeft, rotDegreeListForLeft, color="red", lw=4, linestyle="--", label="$Left\ Turn$")
    turnSeparateAxe.plot(timeListForUTurn, rotDegreeListForUTurn, color="blue", lw=2, linestyle="-", label="$U-Turn$")
    plt.legend(loc=2)

    walkSeparateAxe = fig.add_subplot(132)
    walkSeparateAxe.set_ylim(-2.0, 2.0)
    walkSeparateAxe.yaxis.set_major_locator(MultipleLocator(1.0))
    walkSeparateAxe.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
    walkSeparateAxe.yaxis.set_minor_locator(MultipleLocator(0.5))
    walkSeparateAxe.set_xticks([]) # Hidden the x ticks
    walkSeparateAxe.set_ylabel("$Rot. Rat.$")
    # For the publication of a paper version (Just white or black)
    # walkSeparateAxe.plot(timeListForNW, valueListForNW, color="black", lw=4, linestyle="--", label="$Normal\ Walking$")
    # walkSeparateAxe.plot(timeListForTurns, valueListForTurns, color="black", lw=2, linestyle="-", label="$Turns$")
    walkSeparateAxe.plot(timeListForNW, valueListForNW, color="red", lw=4, linestyle="--", label="$Normal\ Walking$")
    walkSeparateAxe.plot(timeListForTurns, valueListForTurns, color="blue", lw=2, linestyle="-", label="$Turns$")
    plt.legend(loc=4)

    statSeparateAxe = fig.add_subplot(133)
    statSeparateAxe.set_ylim(-0.25, 3.0)
    statSeparateAxe.yaxis.set_major_locator(MultipleLocator(1.0))
    statSeparateAxe.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
    statSeparateAxe.yaxis.set_minor_locator(MultipleLocator(0.25))
    statSeparateAxe.set_xticks([]) # Hidden the x ticks
    statSeparateAxe.set_ylabel("$Var. Acc.$")
    # For the publication of a paper version (Just white or black)
    # statSeparateAxe.plot(timeListForStat, valueListForStat, color="black", lw=4, linestyle="--", label="$Stationary$")
    # statSeparateAxe.plot(timeListForWalk, valueListForWalk, color="black", lw=2, linestyle="-", label="$Walking$")
    statSeparateAxe.plot(timeListForStat, valueListForStat, color="red", lw=4, linestyle="--", label="$Stationary$")
    statSeparateAxe.plot(timeListForWalk, valueListForWalk, color="blue", lw=2, linestyle="-", label="$Walking$")
    plt.legend(loc=2)

    plt.show()

    print("Done.")