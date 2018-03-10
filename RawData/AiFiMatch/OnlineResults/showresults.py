# -*- coding: utf-8 -*-
import string
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import  MultipleLocator, FormatStrFormatter

import pandas as pd

# Environment Configuration
matplotlib.rcParams['font.size'] = 20

def loadErrorData(positionErrorFilePath):
    positionErrorFilePath = unicode(positionErrorFilePath, "utf-8")
    errorList = []
    with open(positionErrorFilePath, "r") as errorFile:
        for record in errorFile:
            errorList.append(string.atof(record.strip()))
    return errorList

if __name__ == "__main__":
    pdrErrorRT1FilePath = "t1_2_20180302213910_route_error_pdr.csv"
    pdrErrorRT2FilePath = "t2_2_20180303165821_route_error_pdr.csv"
    pdrErrorRT3FilePath = "t3_4_20180303143913_route_error_pdr.csv"

    hmmErrorRT1FilePath = "20180302213910_route_error_pdr_online.csv"
    hmmErrorRT2FilePath = "20180303165821_route_error_pdr_online.csv"
    hmmErrorRT3FilePath = "20180303143913_route_error_pdr.csv"

    hmmErrorRT1FilePath = "20180302213910_route_error_aifi_online_0305.csv"
    hmmErrorRT2FilePath = "20180303165821_route_error_aifi_online_0305.csv"
    hmmErrorRT3FilePath = "20180303143913_route_error_aifi_online_0305.csv"

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
    rtOneAxe = plt.subplot(131)
    oneYMajorLocator = MultipleLocator(10.0)
    oneYMajorFormatter = FormatStrFormatter("%.1f")
    oneYMinorLocator = MultipleLocator(4)
    oneXMajorLocator = MultipleLocator(50)
    oneXMajorFormatter = FormatStrFormatter("%d")
    oneXMinorLocator = MultipleLocator(25)
    rtOneAxe.yaxis.set_major_locator(oneYMajorLocator)
    rtOneAxe.yaxis.set_major_formatter(oneYMajorFormatter)
    rtOneAxe.yaxis.set_minor_locator(oneYMinorLocator)
    rtOneAxe.xaxis.set_major_locator(oneXMajorLocator)
    rtOneAxe.xaxis.set_major_formatter(oneXMajorFormatter)
    rtOneAxe.xaxis.set_minor_locator(oneXMinorLocator)
    rtOneAxe.set_xlabel("$Step\ Number$")
    rtOneAxe.set_ylabel("$Position\ Error(m)$")
    rtOneAxe.set_title("(a)")
    #rtOneAxe.set_title("$(a)Position\ Error\ of\ Route\ 1$")
    rtOnePDR, = rtOneAxe.plot(range(len(perOneList)), perOneList, color="blue", lw=2, linestyle="--", label="Basic PDR")
    rtOneHMM, = rtOneAxe.plot(range(len(herOneList)), herOneList, color="red", lw=2, linestyle="-", label="AiFiMatch")
    #rtOneAxe.legend(loc="best", fontsize=20)
    rtOneAxe.legend(loc="best")
    plt.grid()

    rtTwoAxe = plt.subplot(132)
    twoYMajorLocator = MultipleLocator(10)
    twoYMajorFormatter = FormatStrFormatter("%.1f")
    twoYMinorLocator = MultipleLocator(4.0)
    twoXMajorLocator = MultipleLocator(20)
    twoXMajorFormatter = FormatStrFormatter("%d")
    twoXMinorLocator = MultipleLocator(10)
    rtTwoAxe.yaxis.set_major_locator(twoYMajorLocator)
    rtTwoAxe.yaxis.set_major_formatter(twoYMajorFormatter)
    rtTwoAxe.yaxis.set_minor_locator(twoYMinorLocator)
    rtTwoAxe.xaxis.set_major_locator(twoXMajorLocator)
    rtTwoAxe.xaxis.set_major_formatter(twoXMajorFormatter)
    rtTwoAxe.xaxis.set_minor_locator(twoXMinorLocator)
    rtTwoAxe.set_xlabel("$Step\ Number$")
    rtTwoAxe.set_ylabel("$Position\ Error(m)$")
    rtTwoAxe.set_title("(b)")
    #rtTwoAxe.set_title("$(b)Position\ Error\ of\ Route\ 2$")
    rtTwoPDR, = rtTwoAxe.plot(range(len(perTwoList)), perTwoList, color="blue", lw=2, linestyle="--", label="Basic PDR")
    rtTwoHMM, = rtTwoAxe.plot(range(len(herTwoList)), herTwoList, color="red", lw=2, linestyle="-", label="AiFiMatch")
    rtTwoAxe.legend(loc="best")
    plt.grid()

    rtThreeAxe = plt.subplot(133)
    threeYMajorLocator = MultipleLocator(10.0)
    threeYMajorFormatter = FormatStrFormatter("%.1f")
    threeYMinorLocator = MultipleLocator(4)
    threeXMajorLocator = MultipleLocator(50)
    threeXMajorFormatter = FormatStrFormatter("%d")
    threeXMinorLocator = MultipleLocator(25)
    rtThreeAxe.yaxis.set_major_locator(threeYMajorLocator)
    rtThreeAxe.yaxis.set_major_formatter(threeYMajorFormatter)
    rtThreeAxe.yaxis.set_minor_locator(threeYMinorLocator)
    rtThreeAxe.xaxis.set_major_locator(threeXMajorLocator)
    rtThreeAxe.xaxis.set_major_formatter(threeXMajorFormatter)
    rtThreeAxe.xaxis.set_minor_locator(threeXMinorLocator)
    rtThreeAxe.set_xlabel("$Step\ Number$")
    rtThreeAxe.set_ylabel("$Position\ Error(m)$")
    rtThreeAxe.set_title("(c)")
    #rtThreeAxe.set_title("$(c)Position\ Error\ of\ Route\ 3$")
    rtThreePDR, = rtThreeAxe.plot(range(len(perThreeList)), perThreeList, color="blue", lw=2,
                                  linestyle="--", label="Basic PDR")
    rtThreeHMM, = rtThreeAxe.plot(range(len(herThreeList)), herThreeList, color="red", lw=2,
                                  linestyle="-", label="AiFiMatch")
    rtThreeAxe.legend(loc="best")
    plt.grid()

    plt.show()
    print("Done.")