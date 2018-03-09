#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/3/6 下午11:19
@author: Pete
@email: yuwp_1985@163.com
@file: convergehistogram.py.py
@software: PyCharm Community Edition
"""

import math
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys

matplotlib.rcParams['font.size'] = 15

def drawHistogram(dataGroups, colors, patterns, labels, xTicks):

    fig = plt.figure()
    axCvg = fig.add_subplot(111)

    index = np.arange(len(dataGroups))
    bar_width = 0.20
    opacity = 0.4
    for i, dataGroup in enumerate(dataGroups):
        rectArray = axCvg.bar(index + i * bar_width, dataGroup, bar_width, alpha=opacity,
                              color=colors[i], hatch=patterns[i], edgecolor="black", label=labels[i])
        for j, rect in enumerate(rectArray):
            h = rect.get_height()
            axCvg.text(rect.get_x() + rect.get_width() / 2, h,
                       "%.1f" % (dataGroup[j]) if math.fabs(dataGroup[j] - 84.6) > sys.float_info.epsilon else "$\infty$",
                       ha="center", va="bottom")

    plt.ylabel('$Traveled\ Distance(m)$')
    plt.xticks(index + bar_width, xTicks)
    plt.ylim(0,140)
    plt.legend(loc="best", fontsize="15")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    asmmValues = (56, 84.6, 56.9)
    aifiNoWifiValues = (56.7, 84.6, 57.6)
    aifiWithWifiValues = (56.7,23.3,15.0)
    dataGroups = [asmmValues, aifiNoWifiValues, aifiWithWifiValues]
    colorList = ['#0007ff', '#550055', '#ff0033']
    patterns = ["/", "\\", "x", "o", "O", ".", "*", "-", "+", "|"]
    labels = ['Zhou et al.', 'AiFiMatch without Wi-Fi', 'AiFiMatch with Wi-Fi']
    xTicks = ['$T_1$', '$T_2$', '$T_3$']
    drawHistogram(dataGroups, colorList, patterns, labels, xTicks)
    print("Done.")