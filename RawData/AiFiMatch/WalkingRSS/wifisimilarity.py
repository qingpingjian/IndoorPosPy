#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/5/10 10:38
@author: Pete
@email: yuwp_1985@163.com
@file: wifisimilarity.py
@software: PyCharm Community Edition
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib.ticker import  MultipleLocator, FormatStrFormatter


# Environment Configuration
# matplotlib.rcParams['font.size'] = 10
# matplotlib.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签
# matplotlib.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

firstFont = {
    'family': 'serif',
    'color': 'black',
    'weight': 'normal',
    'size': 22,
    }
tickFontSize = 22

if __name__ == "__main__":
    jcd360n5SameFile = "20180509165726_wifi_jaccard_same_360n5_0509.csv"
    jcd360n5DiffFile = "20180509220813_wifi_jaccard_diff_360n5_0510.csv"
    jcdOppor827tSameFile = "20180509200222_wifi_jaccard_same_oppor827t_0509.csv"
    jcdOppor827tDiffFile = "20180509223304_wifi_jaccard_diff_oppor827t_0510.csv"
    jcdXiaomi3wSameFile = "20180510172115_wifi_jaccard_same_xiaomi3w_0511.csv"
    jcdXiaomi3wDiffFile = "20180510175944_wifi_jaccard_diff_xiaomi3w_0511.csv"

    # 360 N5
    jcd360n5SameDF = pd.read_csv(jcd360n5SameFile)
    jcd360n5SameArray = jcd360n5SameDF.values
    jcd360n5DiffDF = pd.read_csv(jcd360n5DiffFile)
    jcd360n5DiffArray = jcd360n5DiffDF.values

    # OPPO R827T
    jcdOppoSameDF = pd.read_csv(jcdOppor827tSameFile)
    jcdOppoSameArray = jcdOppoSameDF.values
    jcdOppoDiffDF = pd.read_csv(jcdOppor827tDiffFile)
    jcdOppoDiffArray = jcdOppoDiffDF.values

    # Xiaomi 3W
    jcdXiaomiSameDF = pd.read_csv(jcdXiaomi3wSameFile)
    jcdXiaomiSameArray = jcdXiaomiSameDF.values
    jcdXiaomiDiffDF = pd.read_csv(jcdXiaomi3wDiffFile)
    jcdXiaomiDiffArray = jcdXiaomiDiffDF.values

    # Borders
    maxSameThreshold = float(np.max(jcdOppoSameArray[:, 1]))
    print maxSameThreshold

    # Plot the axes
    fig = plt.figure()
    jcd360Axe = plt.subplot(131)
    jcd360Axe.plot(jcd360n5SameArray[:, 0], jcd360n5SameArray[:, 1], "b-", linewidth=2)
    jcd360Axe.plot(jcd360n5SameArray[:, 0], jcd360n5SameArray[:, 2], "b-", linewidth=2)
    jcd360Axe.fill_between(jcd360n5SameArray[:, 0], jcd360n5SameArray[:, 1], jcd360n5SameArray[:, 2], alpha=0.35, hatch="\\", edgecolor="black", label="$Same\ Segments$")
    jcd360Axe.plot(jcd360n5DiffArray[:, 0], jcd360n5DiffArray[:, 1], "g-", linewidth=2)
    jcd360Axe.plot(jcd360n5DiffArray[:, 0], jcd360n5DiffArray[:, 2], "g-", linewidth=2)
    jcd360Axe.fill_between(jcd360n5DiffArray[:, 0], jcd360n5DiffArray[:, 1], jcd360n5DiffArray[:, 2], alpha=0.35, hatch="/", edgecolor="black", label="$Different\ Segments$")
    jcd360Axe.axhline(round(maxSameThreshold * 1000) / 1000, ls=":", lw=5, color="r")
    jcd360Axe.text(15, round(maxSameThreshold * 1000) / 1000 + 0.01, "$d_{min}=0.773$", fontdict=firstFont)
    jcd360Axe.axvline(5, ls=":", lw=5, color="r")
    jcd360Axe.text(5.5, 0.93, "$w=5$", fontdict=firstFont)
    jcd360Axe.set_xlabel("$Length\ of\ WiFi\ Sequence$", fontdict=firstFont)
    jcd360Axe.set_ylabel("$WiFi\ Sequence\ Dissimilarity$", fontdict=firstFont)
    jcd360Axe.set_title("$(a)\ 360\ N5\ vs.\ 360\ N5$", fontdict=firstFont)
    plt.xticks(fontsize=tickFontSize)
    plt.yticks(fontsize=tickFontSize)
    jcd360Axe.set_xlim(0, 45)
    jcd360Axe.set_ylim(0.3, 1.0)
    jcd360Axe.grid(True)
    jcd360Axe.legend(loc=7, fontsize=tickFontSize)

    jcdOppoAxe = plt.subplot(132)
    jcdOppoAxe.plot(jcdOppoSameArray[:, 0], jcdOppoSameArray[:, 1], "b-", linewidth=2)
    jcdOppoAxe.plot(jcdOppoSameArray[:, 0], jcdOppoSameArray[:, 2], "b-", linewidth=2)
    jcdOppoAxe.fill_between(jcdOppoSameArray[:, 0], jcdOppoSameArray[:, 1], jcdOppoSameArray[:, 2], alpha=0.35, hatch="\\", edgecolor="black", label="$Same\ Segments$")
    jcdOppoAxe.plot(jcdOppoDiffArray[:, 0], jcdOppoDiffArray[:, 1], "g-", linewidth=2)
    jcdOppoAxe.plot(jcdOppoDiffArray[:, 0], jcdOppoDiffArray[:, 2], "g-", linewidth=2)
    jcdOppoAxe.fill_between(jcdOppoDiffArray[:, 0], jcdOppoDiffArray[:, 1], jcdOppoDiffArray[:, 2], alpha=0.35, hatch="/", edgecolor="black", label="$Different\ Segments$")
    # jcdDistAxes.axvline(t, ls=":", lw=2, color="#FF00CC") 0.63
    jcdOppoAxe.axhline(round(maxSameThreshold * 1000) / 1000, ls=":", lw=5, color="r")
    jcdOppoAxe.text(14, round(maxSameThreshold * 1000) / 1000 + 0.01, "$d_{min}=0.773$", fontdict=firstFont)
    jcdOppoAxe.set_xlabel("$Length\ of\ WiFi\ Sequence$", fontdict=firstFont)
    jcdOppoAxe.set_ylabel("$WiFi\ Sequence\ Dissimilarity$", fontdict=firstFont)
    jcdOppoAxe.set_title("$(b) 360\ N5\ vs.\ OPPO\ R827T$", fontdict=firstFont)
    plt.xticks(fontsize=tickFontSize)
    plt.yticks(fontsize=tickFontSize)
    jcdOppoAxe.set_xlim(0, 40)
    jcdOppoAxe.set_ylim(0.3, 1.0)
    jcdOppoAxe.grid(True)
    jcdOppoAxe.legend(loc=4, fontsize=tickFontSize)

    jcdXiaomiAxe = plt.subplot(133)
    jcdXiaomiAxe.plot(jcdXiaomiSameArray[:, 0], jcdXiaomiSameArray[:, 1], "b-", linewidth=2)
    jcdXiaomiAxe.plot(jcdXiaomiSameArray[:, 0], jcdXiaomiSameArray[:, 2], "b-", linewidth=2)
    jcdXiaomiAxe.fill_between(jcdXiaomiSameArray[:, 0], jcdXiaomiSameArray[:, 1], jcdXiaomiSameArray[:, 2], alpha=0.35, hatch="\\", edgecolor="black", label="$Same\ Segments$")
    jcdXiaomiAxe.plot(jcdXiaomiDiffArray[:, 0], jcdXiaomiDiffArray[:, 1], "g-", linewidth=2)
    jcdXiaomiAxe.plot(jcdXiaomiDiffArray[:, 0], jcdXiaomiDiffArray[:, 2], "g-", linewidth=2)
    jcdXiaomiAxe.fill_between(jcdXiaomiDiffArray[:, 0], jcdXiaomiDiffArray[:, 1], jcdXiaomiDiffArray[:, 2], alpha=0.35, hatch="/", edgecolor="black", label="$Different\ Segments$")
    jcdXiaomiAxe.axhline(round(maxSameThreshold * 1000) / 1000, ls=":", lw=5, color="r")
    jcdXiaomiAxe.text(22, round(maxSameThreshold * 1000) / 1000 - 0.05, "$d_{min}=0.773$", fontdict=firstFont)
    jcdXiaomiAxe.axvline(11, ls=":", lw=5, color="r")
    jcdXiaomiAxe.text(11.5, 0.93, "$w=11$", fontdict=firstFont)
    jcdXiaomiAxe.set_xlabel("$Length\ of\ WiFi\ Sequence$", fontdict=firstFont)
    jcdXiaomiAxe.set_ylabel("$WiFi\ Sequence\ Dissimilarity$", fontdict=firstFont)
    jcdXiaomiAxe.set_title("$(c)\ 360\ N5\ vs.\ Xiaomi\ 3W$", fontdict=firstFont)
    plt.xticks(fontsize=tickFontSize)
    plt.yticks(fontsize=tickFontSize)
    jcdXiaomiAxe.set_xlim(0, 40)
    jcdXiaomiAxe.set_ylim(0.3, 1.0)
    jcdXiaomiAxe.grid(True)
    jcdXiaomiAxe.legend(loc=7, fontsize=tickFontSize)
    plt.show()
    print("Done.")