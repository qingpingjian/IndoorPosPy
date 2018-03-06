# -*- coding: utf-8 -*-
import string
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import  MultipleLocator, FormatStrFormatter

# Environment Configuration
matplotlib.rcParams['font.size'] = 30

def loadErrorData(positionErrorFilePath):
    positionErrorFilePath = unicode(positionErrorFilePath, "utf-8")
    errorList = []
    with open(positionErrorFilePath, "r") as errorFile:
        for record in errorFile:
            errorList.append(string.atof(record.strip()))
    return errorList

if __name__ == "__main__":
    pdrErrorRT1FilePath = "./RouteOne/20170702201525_route1_err_pdr.txt"
    pdrErrorRT2FilePath = "./RouteTwo/20170702201525_route2_err_pdr.txt"
    pdrErrorRT3FilePath = "./RouteThree/20170702201525_route3_err_pdr.txt"
    pdrErrorRT4FilePath = "./RouteFour/20170702201525_route4_err_pdr.txt"

    hmmErrorRT1FilePath = "./RouteOneSub/20170702201525_route1_err_pdr.txt"
    hmmErrorRT2FilePath = "./RouteTwoSub/20170702201525_route2_err_pdr.txt"
    hmmErrorRT3FilePath = "./RouteThreeSub/20170702201525_route3_err_pdr.txt"
    hmmErrorTR4FilePath = "./RouteFourSub/20170702201525_route4_err_pdr.txt"

    perOneList = loadErrorData(pdrErrorRT1FilePath)
    herOneList = loadErrorData(hmmErrorRT1FilePath)

    perTwoList = loadErrorData(pdrErrorRT2FilePath)
    herTwoList = loadErrorData(hmmErrorRT2FilePath)

    perThreeList = loadErrorData(pdrErrorRT3FilePath)
    herThreeList = loadErrorData(hmmErrorRT3FilePath)

    perFourList = loadErrorData(pdrErrorRT4FilePath)
    herFourList = loadErrorData(hmmErrorTR4FilePath)

    # Plot the axes
    fig = plt.figure()
    rtOneAxe = plt.subplot(221)
    oneYMajorLocator = MultipleLocator(1.0)
    oneYMajorFormatter = FormatStrFormatter("%.1f")
    oneYMinorLocator = MultipleLocator(0.5)
    oneXMajorLocator = MultipleLocator(10)
    oneXMajorFormatter = FormatStrFormatter("%d")
    oneXMinorLocator = MultipleLocator(5)
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
    rtOnePDR, = rtOneAxe.plot(range(len(perOneList)), perOneList, color="blue", lw=7, linestyle="--", label="PDR")
    rtOneHMM, = rtOneAxe.plot(range(len(herOneList)), herOneList, color="red", lw=7, linestyle="-", label="PDR+HMM")
    rtOneAxe.legend(loc="best", fontsize=20)
    plt.grid()

    rtTwoAxe = plt.subplot(222)
    twoYMajorLocator = MultipleLocator(3.5)
    twoYMajorFormatter = FormatStrFormatter("%.1f")
    twoYMinorLocator = MultipleLocator(1.0)
    twoXMajorLocator = MultipleLocator(30)
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
    rtTwoPDR, = rtTwoAxe.plot(range(len(perTwoList)), perTwoList, color="blue", lw=7, linestyle="--", label="PDR")
    rtTwoHMM, = rtTwoAxe.plot(range(len(herTwoList)), herTwoList, color="red", lw=7, linestyle="-", label="PDR+HMM")
    rtTwoAxe.legend(loc=2, fontsize=20)
    plt.grid()

    rtThreeAxe = plt.subplot(223)
    threeYMajorLocator = MultipleLocator(1.0)
    threeYMajorFormatter = FormatStrFormatter("%.1f")
    threeYMinorLocator = MultipleLocator(0.5)
    threeXMajorLocator = MultipleLocator(10)
    threeXMajorFormatter = FormatStrFormatter("%d")
    threeXMinorLocator = MultipleLocator(5)
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
    rtThreePDR, = rtThreeAxe.plot(range(len(perThreeList)), perThreeList, color="blue", lw=7,
                                  linestyle="--", label="PDR")
    rtThreeHMM, = rtThreeAxe.plot(range(len(herThreeList)), herThreeList, color="red", lw=7,
                                  linestyle="-", label="PDR+HMM")
    rtThreeAxe.legend(loc="best", fontsize=20)
    plt.grid()

    rtFourAxe = plt.subplot(224)
    fourYMajorLocator = MultipleLocator(2.0)
    fourYMajorFormatter = FormatStrFormatter("%.1f")
    fourYMinorLocator = MultipleLocator(1.0)
    fourXMajorLocator = MultipleLocator(20)
    fourXMajorFormatter = FormatStrFormatter("%d")
    fourXMinorLocator = MultipleLocator(10)
    rtFourAxe.yaxis.set_major_locator(fourYMajorLocator)
    rtFourAxe.yaxis.set_major_formatter(fourYMajorFormatter)
    rtFourAxe.yaxis.set_minor_locator(fourYMinorLocator)
    rtFourAxe.xaxis.set_major_locator(fourXMajorLocator)
    rtFourAxe.xaxis.set_major_formatter(fourXMajorFormatter)
    rtFourAxe.xaxis.set_minor_locator(fourXMinorLocator)
    rtFourAxe.set_xlabel("$Step\ Number$")
    rtFourAxe.set_ylabel("$Position\ Error(m)$")
    rtFourAxe.set_title("(d)")
    #rtFourAxe.set_title("$(d)Position\ Error\ of\ Route\ 4$")
    rtFourPDR, = rtFourAxe.plot(range(len(perFourList)), perFourList, color="blue", lw=7, linestyle="--", label="PDR")
    rtFourWiFi, = rtFourAxe.plot(range(len(herFourList)), herFourList, color="red", lw=7,
                                  linestyle="-", label="PDR+HMM")
    rtFourAxe.legend(loc="best", fontsize=20)
    plt.grid()

    plt.show()
    print("Done.")