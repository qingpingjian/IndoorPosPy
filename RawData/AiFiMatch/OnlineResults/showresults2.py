# -*- coding: utf-8 -*-
import string
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import  MultipleLocator, FormatStrFormatter

import pandas as pd

# Environment Configuration
matplotlib.rcParams['font.size'] = 18

firstFont = {
    'family': 'Times New Roman',
    'color': 'black',
    'weight': 'normal',
    'size': 18,
    }

def loadErrorData(positionErrorFilePath):
    positionErrorFilePath = unicode(positionErrorFilePath, "utf-8")
    errorList = []
    with open(positionErrorFilePath, "r") as errorFile:
        for record in errorFile:
            errorList.append(string.atof(record.strip()))
    return errorList

if __name__ == "__main__":
    pdrErrorRT1FilePath = "20180302213910_route_error_pdr_t1_2.csv"
    pdrErrorRT2FilePath = "20180303165821_route_error_pdr_t2_2.csv"
    pdrErrorRT3FilePath = "20180303143913_route_error_pdr_t3_4.csv"

    hmmErrorRT1FilePath = "20180302213910_route_error_aifi_online_0305.csv"
    hmmErrorRT2FilePath = "20180303165821_route_error_aifi_online_0305.csv"
    hmmErrorRT3FilePath = "20180303143913_route_error_aifi_online_0305.csv"

    hmmErrorRT1FilePath = "20180302213910_error_aifi_online_0315.csv"
    hmmErrorRT2FilePath = "20180303165821_route_error_aifi_online_0305.csv"
    hmmErrorRT3FilePath = "20180303143913_error_aifi_online_0314.csv"

    perOneDF = pd.read_csv(pdrErrorRT1FilePath)
    perOneList = perOneDF.values
    herOneDF = pd.read_csv(hmmErrorRT1FilePath)
    herOneList = herOneDF.values

    perTwoDF = pd.read_csv(pdrErrorRT2FilePath)
    perTwoList = perTwoDF.values
    herTwoDF = pd.read_csv(hmmErrorRT2FilePath)
    herTwoList = herTwoDF.values

    perThreeDF = pd.read_csv(pdrErrorRT3FilePath)
    perThreeList = perThreeDF.values
    herThreeDF = pd.read_csv(hmmErrorRT3FilePath)
    herThreeList = herThreeDF.values

    # Plot the axes
    fig = plt.figure()
    plt.rc('font', family='Times New Roman')
    colorGroup = ["blue", "red"]
    colorGroup = ["#000000", "#000000"]

    rtOneAxe = plt.subplot(311)
    rtOneAxe.set_xlim(0, 250)
    rtOneAxe.set_ylim(0.0, 40.0)
    rtOneAxe.yaxis.set_major_locator(MultipleLocator(10.0))
    rtOneAxe.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
    # rtOneAxe.yaxis.set_minor_locator(MultipleLocator(5.0))
    rtOneAxe.xaxis.set_major_locator(MultipleLocator(50))
    rtOneAxe.xaxis.set_major_formatter(FormatStrFormatter("%d"))
    rtOneAxe.xaxis.set_minor_locator(MultipleLocator(25))
    rtOneAxe.set_xlabel("Step Number")
    rtOneAxe.set_ylabel("Position Error(m)")
    rtOneAxe.set_title("(a)")
    rtOnePDR, = rtOneAxe.plot(range(len(perOneList)), perOneList, color=colorGroup[0], lw=2, linestyle="--", label="Basic PDR")
    rtOneHMM, = rtOneAxe.plot(range(len(herOneList)), herOneList, color=colorGroup[1], lw=2, linestyle="-", label="AiFiMatch")
    rtOneAxe.legend(loc="best")
    plt.grid()

    rtTwoAxe = plt.subplot(312)
    rtTwoAxe.set_xlim(0, 120)
    rtTwoAxe.set_ylim(0.0, 40.0)
    rtTwoAxe.yaxis.set_major_locator(MultipleLocator(10.0))
    rtTwoAxe.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
    # rtTwoAxe.yaxis.set_minor_locator(MultipleLocator(5.0))
    rtTwoAxe.xaxis.set_major_locator(MultipleLocator(20))
    rtTwoAxe.xaxis.set_major_formatter(FormatStrFormatter("%d"))
    rtTwoAxe.set_xlabel("Step Number")
    rtTwoAxe.set_ylabel("Position Error(m)")
    rtTwoAxe.set_title("(b)")
    rtTwoPDR, = rtTwoAxe.plot(range(len(perTwoList)), perTwoList, color=colorGroup[0], lw=2,
                              linestyle="--", label="Basic PDR")
    rtTwoHMM, = rtTwoAxe.plot(range(len(herTwoList)), herTwoList, color=colorGroup[1], lw=2,
                              linestyle="-", label="AiFiMatch")
    rtTwoAxe.legend(loc="best")
    plt.grid()

    rtThreeAxe = plt.subplot(313)
    rtThreeAxe.set_xlim(0, 250)
    rtThreeAxe.set_ylim(0.0, 40.0)
    rtThreeAxe.yaxis.set_major_locator(MultipleLocator(10.0))
    rtThreeAxe.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
    # rtThreeAxe.yaxis.set_minor_locator(MultipleLocator(5.0))
    rtThreeAxe.xaxis.set_major_locator(MultipleLocator(50))
    rtThreeAxe.xaxis.set_major_formatter(FormatStrFormatter("%d"))
    rtThreeAxe.set_xlabel("Step Number")
    rtThreeAxe.set_ylabel("Position Error(m)")
    rtThreeAxe.set_title("(c)")
    rtThreePDR, = rtThreeAxe.plot(range(len(perThreeList)), perThreeList, color=colorGroup[0], lw=2,
                                  linestyle="--", label="Basic PDR")
    rtThreeHMM, = rtThreeAxe.plot(range(len(herThreeList)), herThreeList, color=colorGroup[1], lw=2,
                                  linestyle="-", label="AiFiMatch")
    rtThreeAxe.legend(loc="best")
    plt.grid()

    plt.show()
    print("Done.")