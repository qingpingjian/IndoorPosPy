# -*- coding: utf-8 -*-
"""
Created on Sun July 2 10:38:17 2017
@author: Wenping

"""
import csv
import math
import random as rd

def genLocation(startPoint, endPoint, num, recalibrate=True):
    locList = []
    locList.append(startPoint)
    if math.fabs(startPoint[0] - endPoint[0]) < 0.0001:
        stepLength = (endPoint[1] - startPoint[1]) / num
        print("Step Length: %.2f" % (stepLength))
        for i in range(1, num + 1):
            x = startPoint[0] + rd.gauss(0.0, 0.07) if recalibrate else 0.0
            y = startPoint[1] + stepLength * i + rd.gauss(0.0, 0.08) if recalibrate else 0.0
            locList.append((x, y))
    elif math.fabs(startPoint[1] - endPoint[1]) < 0.0001:
        stepLength = (endPoint[0] - startPoint[0]) / num
        print("Step Length: %.2f" % (stepLength))
        for i in range(1, num + 1):
            x = startPoint[0] + stepLength * i + rd.gauss(0.0, 0.08) if recalibrate else 0.0
            y = startPoint[1] + rd.gauss(0.0, 0.07) if recalibrate else 0.0
            locList.append((x, y))
    print("Step Number: %d VS. %d" % (num, len(locList) - 1) )
    for loc in locList:
        print("%.3f, %.3f" % loc)
    return
if __name__ == "__main__":
    # Path A->B
    sp = (1.2, 1.7)
    ep = (1.2, 10.7)
    genLocation(sp, ep, 13)