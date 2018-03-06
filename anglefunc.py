#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/3/6 15:19
@author: Pete
@email: yuwp_1985@163.com
@file: anglefunc.py
@software: PyCharm Community Edition
"""
import math

"""
General functions to deal with angles
"""

def angleNormalize(angle):
    """
    Keep angle in {0, 2pi)
    :param angle:
    :return: Normalized angle value
    """
    return (angle % (2.0 * math.pi) + 2.0 * math.pi) % (2.0 * math.pi)


def meanAngle(angleList, normalize = True):
    """
    Calculate the average of a set of circular data in radian
    :param angleList: a set of circular data
    :return: average value in radian
    """
    sinSum = 0
    cosSum = 0
    for angle in angleList:
        sinSum += math.sin(angle)
        cosSum += math.cos(angle)
    meanValue = math.atan2(sinSum, cosSum)
    return angleNormalize(meanValue) if normalize else meanValue


"""
General functions to deal with walking directions
"""

DHT = (50.0 * math.pi) / 180.0  # Threshold for the delta of direction
def isHeadingMatch(headingDir, baseDirection):
    headingDir = angleNormalize(headingDir) # [0, 2pi)
    baseDirection = angleNormalize(baseDirection) # [0, 2pi)
    diffAngle = headingDir - baseDirection if headingDir >= baseDirection else baseDirection - headingDir
    if diffAngle > math.pi:
        diffAngle -= 2.0 * math.pi
    return True if math.fabs(diffAngle) < DHT else False


if __name__ == "__main__":
    print("Done.")