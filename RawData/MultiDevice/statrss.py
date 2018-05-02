#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/5/2 9:14
@author: Pete
@email: yuwp_1985@163.com
@file: statrss.py
@software: PyCharm Community Edition
"""
import collections
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib.ticker import  MultipleLocator, FormatStrFormatter

matplotlib.rcParams['font.size'] = 15
matplotlib.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

def autolabel(figAxes, rects, txtRot=90):
    for rect in rects:
        height = rect.get_height()
        if height >= 0.01:
            figAxes.text(rect.get_x() + rect.get_width() / 2. - 0.1, height + 0.034, '%.2f%%' % (float(height) * 100.0), rotation=txtRot)
    return

def rssHist(fileName, macAddr):
    wifiDF = pd.read_csv(fileName)
    rssDF = wifiDF.ix[:,["wifiinfos"]]
    rssValueList = []
    for rssStr in rssDF.values:
        rssList = [rssRecord.split("|") for rssRecord in rssStr[0].split(';')]
        for rss in rssList:
            if rss[0] == macAddr:
                rssValueList.append(rss[1])
    # Counting the frequency of values
    rssFreqDict = collections.Counter(rssValueList)
    rssLength = len(rssValueList)
    rssStrList = sorted(rssFreqDict.keys(), reverse=True)
    freqList = [round(rssFreqDict.get(rssStr) * 1.0 / rssLength, 4) for rssStr in rssStrList]
    values = [float(v) for v in rssStrList]
    print np.mean(values)
    print freqList
    xMin = min(values) - 1.0
    xMax = max(values) + 1.0
    yMin = 0.0
    yMax = round(max(freqList) + 0.05, 1)

    # Show the histogram of rss values
    fig = plt.figure()
    freqAxe = fig.add_subplot(111)
    freqRects = freqAxe.bar(values, freqList, width=0.8)
    autolabel(freqAxe, freqRects)
    freqAxe.set_xlim(xMin, xMax)
    freqAxe.xaxis.set_major_locator(MultipleLocator(2))
    freqAxe.xaxis.set_major_formatter(FormatStrFormatter("%d"))
    freqAxe.xaxis.set_minor_locator(MultipleLocator(1))
    freqAxe.set_ylim(yMin, yMax)
    freqAxe.set_title("RSS Value Statistics")
    freqAxe.set_xlabel("RSS Values(dBm)")
    freqAxe.set_ylabel("Frequency")
    plt.grid(False)
    plt.show()

    return

if __name__ == "__main__":
    rssFileName = "20180427163534_wifi.csv"
    rssFileName = "20180429161018_wifi.csv"
    macAddr = "50:64:2b:7b:07:92"
    rssHist(rssFileName, macAddr)
    print("Done.")