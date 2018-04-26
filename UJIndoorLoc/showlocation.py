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

def showLoc(wifiFile, colFilterList):
    wifiDF = pd.read_csv(wifiFile)
    locArray = wifiDF.ix[:, colFilterList].values
    maxValues = np.max(locArray, axis=0)
    print(maxValues)
    minValues = np.min(locArray, axis=0)
    print(minValues)
    # acceDF.ix[:,['timestamp', 'acce_x', 'acce_y', 'acce_z']]
    pass

if __name__ == "__main__":
    wifiFPFile = "trainingData.csv"
    headingFilterList = ["LONGITUDE", "LATITUDE"]

    showLoc(wifiFPFile, headingFilterList)

    print("Done.")