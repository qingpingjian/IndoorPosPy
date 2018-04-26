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
import random as rd

def spaceSave(wifiFingerprintFile):
    headings = ["BUILDINGID", "FLOOR", "SPACEID"]
    newHeadings = ["FLOORCODE", "SPACEID"]
    wifiDF = pd.read_csv(wifiFingerprintFile)
    spaceArray = wifiDF.ix[:, headings].values.astype(np.int32)
    spaceDF = pd.DataFrame(np.column_stack((spaceArray[:,0] * 10 + spaceArray[:,1], spaceArray[:,2])), columns=newHeadings)
    spaceDF.to_csv("trainingSpace.csv", encoding='utf-8', index=False)
    return

def showLoc(wifiFile, colFilterList):
    headings = ["LONGITUDE", "LATITUDE", "BUILDINGID", "FLOOR"]

    pass

if __name__ == "__main__":
    wifiTrainFile = "trainingData.csv"
    spaceSave(wifiTrainFile)
    print("Done.")