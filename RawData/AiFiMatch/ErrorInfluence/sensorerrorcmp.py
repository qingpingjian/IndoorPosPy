#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/5/15 19:51
@author: Pete
@email: yuwp_1985@163.com
@file: sensorerrorcmp.py
@software: PyCharm Community Edition
"""
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.ticker import  MultipleLocator, FormatStrFormatter

firstFont = {
    'family': 'serif',
    'color': 'black',
    'weight': 'normal',
    'size': 16,
    }
tickFontSize = 16

if __name__ == "__main__":
    pdrStepT1ErrorFile = "pdr_error_step_t1_0515.csv"
    pdrStepT2ErrorFile = "pdr_error_step_t2_0515.csv"
    pdrStepT3ErrorFile = "pdr_error_step_t3_0515.csv"

    aifiStepT1ErrorFile = "aifi_error_step_t1_0516.csv"
    aifiStepT2ErrorFile = "aifi_error_step_t2_0516.csv"
    aifiStepT3ErrorFile = "aifi_error_step_t3_0516.csv"


    pdrHeadingT1ErrorFile = "pdr_error_heading_t1_0515.csv"
    pdrHeadingT2ErrorFile = "pdr_error_heading_t2_0515.csv"
    pdrHeadingT3ErrorFile = "pdr_error_heading_t3_0515.csv"

    aifiHeadingT1ErrorFile = "aifi_error_heading_t1_0517.csv"
    aifiHeadingT2ErrorFile = "aifi_error_heading_t2_0517.csv"
    aifiHeadingT3ErrorFile = "aifi_error_heading_t3_0517.csv"

    # Step Length Error
    pdrStepT1ErrorDF = pd.read_csv(pdrStepT1ErrorFile)
    pdrStepT1ErrorArray = pdrStepT1ErrorDF.ix[1:, ["Delta_Step", "Error(m)"]].values
    pdrStepT2ErrorDF = pd.read_csv(pdrStepT2ErrorFile)
    pdrStepT2ErrorArray = pdrStepT2ErrorDF.ix[1:, ["Delta_Step", "Error(m)"]].values
    pdrStepT3ErrorDF = pd.read_csv(pdrStepT3ErrorFile)
    pdrStepT3ErrorArray = pdrStepT3ErrorDF.ix[1:, ["Delta_Step", "Error(m)"]].values

    aifiStepT1ErrorDF = pd.read_csv(aifiStepT1ErrorFile)
    aifiStepT1ErrorArray = aifiStepT1ErrorDF.ix[1:, ["Delta_Step", "Error(m)"]].values
    aifiStepT2ErrorDF = pd.read_csv(aifiStepT2ErrorFile)
    aifiStepT2ErrorArray = aifiStepT2ErrorDF.ix[1:, ["Delta_Step", "Error(m)"]].values
    aifiStepT3ErrorDF = pd.read_csv(aifiStepT3ErrorFile)
    aifiStepT3ErrorArray = aifiStepT3ErrorDF.ix[1:, ["Delta_Step", "Error(m)"]].values


    # Heading Error
    pdrHeadingT1ErrorDF = pd.read_csv(pdrHeadingT1ErrorFile)
    pdrHeadingT1ErrArray = pdrHeadingT1ErrorDF.ix[1:, ["Delta_Heading", "Error(m)"]].values
    pdrHeadingT2ErrorDF = pd.read_csv(pdrHeadingT2ErrorFile)
    pdrHeadingT2ErrArray = pdrHeadingT2ErrorDF.ix[1:, ["Delta_Heading", "Error(m)"]].values
    pdrHeadingT3ErrorDF = pd.read_csv(pdrHeadingT3ErrorFile)
    pdrHeadingT3ErrArray = pdrHeadingT3ErrorDF.ix[1:, ["Delta_Heading", "Error(m)"]].values

    aifiHeadingT1ErrorDF = pd.read_csv(aifiHeadingT1ErrorFile)
    aifiHeadingT1ErrArray = aifiHeadingT1ErrorDF.ix[1:, ["Delta_Heading", "Error(m)"]].values
    aifiHeadingT2ErrorDF = pd.read_csv(aifiHeadingT2ErrorFile)
    aifiHeadingT2ErrArray = aifiHeadingT2ErrorDF.ix[1:, ["Delta_Heading", "Error(m)"]].values
    aifiHeadingT3ErrorDF = pd.read_csv(aifiHeadingT3ErrorFile)
    aifiHeadingT3ErrArray = aifiHeadingT3ErrorDF.ix[1:, ["Delta_Heading", "Error(m)"]].values

    # Plot the axes
    fig = plt.figure()
    stepFirstErrAxe = plt.subplot(231)
    stepFirstErrAxe.plot(pdrStepT1ErrorArray[:, 0], pdrStepT1ErrorArray[:, 1], "r-", marker="^", linewidth=2, label="$Basic\ PDR$")
    stepFirstErrAxe.plot(aifiStepT1ErrorArray[:, 0], aifiStepT1ErrorArray[:, 1], "b-", marker="o", linewidth=2, label="$AiFiMatch$")
    stepFirstErrAxe.set_xlabel("$\sigma_s(m)$", fontdict=firstFont)
    stepFirstErrAxe.set_ylabel("$Position\ Error(m)$", fontdict=firstFont)
    stepFirstErrAxe.set_title("$(a)$", fontdict=firstFont)
    stepFirstErrAxe.set_xlim(0.0, 0.6)
    stepFirstErrAxe.set_ylim(0, 8)
    stepFirstErrAxe.yaxis.set_major_locator(MultipleLocator(2))
    stepFirstErrAxe.yaxis.set_minor_locator(MultipleLocator(1))
    plt.xticks(fontsize=tickFontSize)
    plt.yticks(fontsize=tickFontSize)
    stepFirstErrAxe.grid(True)
    stepFirstErrAxe.legend(loc=2, fontsize=tickFontSize)

    stepSecondErrAxe = plt.subplot(232)
    stepSecondErrAxe.plot(pdrStepT2ErrorArray[:, 0], pdrStepT2ErrorArray[:, 1], "r-", marker="^", linewidth=2, label="$Basic\ PDR$")
    stepSecondErrAxe.plot(aifiStepT2ErrorArray[:, 0], aifiStepT2ErrorArray[:, 1], "b-", marker="o", linewidth=2, label="$AiFiMatch$")
    stepSecondErrAxe.set_xlabel("$\sigma_s(m)$", fontdict=firstFont)
    stepSecondErrAxe.set_ylabel("$Position\ Error(m)$", fontdict=firstFont)
    stepSecondErrAxe.set_title("$(b)$", fontdict=firstFont)
    stepSecondErrAxe.set_xlim(0.0, 0.6)
    stepSecondErrAxe.set_ylim(0, 6)
    stepSecondErrAxe.yaxis.set_major_locator(MultipleLocator(2))
    stepSecondErrAxe.yaxis.set_minor_locator(MultipleLocator(1))
    plt.xticks(fontsize=tickFontSize)
    plt.yticks(fontsize=tickFontSize)
    stepSecondErrAxe.grid(True)
    stepSecondErrAxe.legend(loc=2, fontsize=tickFontSize)

    stepThirdErrAxe = plt.subplot(233)
    stepThirdErrAxe.plot(pdrStepT3ErrorArray[:, 0], pdrStepT3ErrorArray[:, 1], "r-", marker="^", linewidth=2, label="$Basic\ PDR$")
    stepThirdErrAxe.plot(aifiStepT3ErrorArray[:, 0], aifiStepT3ErrorArray[:, 1], "b-", marker="o", linewidth=2, label="$AiFiMatch$")
    stepThirdErrAxe.set_xlabel("$\sigma_s(m)$", fontdict=firstFont)
    stepThirdErrAxe.set_ylabel("$Position\ Error(m)$", fontdict=firstFont)
    stepThirdErrAxe.set_title("$(c)$", fontdict=firstFont)
    stepThirdErrAxe.set_xlim(0.0, 0.6)
    stepThirdErrAxe.set_ylim(2, 6)
    stepThirdErrAxe.yaxis.set_major_locator(MultipleLocator(2))
    stepThirdErrAxe.yaxis.set_minor_locator(MultipleLocator(1))
    plt.xticks(fontsize=tickFontSize)
    plt.yticks(fontsize=tickFontSize)
    stepThirdErrAxe.grid(True)
    stepThirdErrAxe.legend(loc=2, fontsize=tickFontSize)

    headingFirstErrAxe = plt.subplot(234)
    headingFirstErrAxe.plot(pdrHeadingT1ErrArray[:, 0], pdrHeadingT1ErrArray[:, 1], "r-", marker="^", linewidth=2, label="$Basic\ PDR$")
    headingFirstErrAxe.plot(aifiHeadingT1ErrArray[:, 0], aifiHeadingT1ErrArray[:, 1], "b-", marker="o", linewidth=2, label="$AiFiMatch$")
    headingFirstErrAxe.set_xlabel(r"$\sigma_{\varphi}(degree)$", fontdict=firstFont)
    headingFirstErrAxe.set_ylabel("$Position\ Error(m)$", fontdict=firstFont)
    headingFirstErrAxe.set_title("$(d)$", fontdict=firstFont)
    headingFirstErrAxe.set_xlim(0, 60)
    headingFirstErrAxe.set_ylim(0, 14)
    headingFirstErrAxe.yaxis.set_major_locator(MultipleLocator(2))
    plt.xticks(fontsize=tickFontSize)
    plt.yticks(fontsize=tickFontSize)
    headingFirstErrAxe.grid(True)
    headingFirstErrAxe.legend(loc=2, fontsize=tickFontSize)

    headingSecondErrAxe = plt.subplot(235)
    headingSecondErrAxe.plot(pdrHeadingT2ErrArray[:, 0], pdrHeadingT2ErrArray[:, 1], "r-", marker="^", linewidth=2, label="$Basic\ PDR$")
    headingSecondErrAxe.plot(aifiHeadingT2ErrArray[:, 0], aifiHeadingT2ErrArray[:, 1], "b-", marker="o", linewidth=2, label="$AiFiMatch$")
    headingSecondErrAxe.set_xlabel(r"$\sigma_{\varphi}(degree)$", fontdict=firstFont)
    headingSecondErrAxe.set_ylabel("$Position\ Error(m)$", fontdict=firstFont)
    headingSecondErrAxe.set_title("$(e)$", fontdict=firstFont)
    headingSecondErrAxe.set_xlim(0, 60)
    headingSecondErrAxe.set_ylim(0, 14)
    headingSecondErrAxe.yaxis.set_major_locator(MultipleLocator(2))
    plt.xticks(fontsize=tickFontSize)
    plt.yticks(fontsize=tickFontSize)
    headingSecondErrAxe.grid(True)
    headingSecondErrAxe.legend(loc=2, fontsize=tickFontSize)

    headingThirdErrAxe = plt.subplot(236)
    headingThirdErrAxe.plot(pdrHeadingT3ErrArray[:, 0], pdrHeadingT3ErrArray[:, 1], "r-", marker="^", linewidth=2, label="$Basic\ PDR$")
    headingThirdErrAxe.plot(aifiHeadingT3ErrArray[:, 0], aifiHeadingT3ErrArray[:, 1], "b-", marker="o", linewidth=2, label="$AiFiMatch$")
    headingThirdErrAxe.set_xlabel(r"$\sigma_{\varphi}(degree)$", fontdict=firstFont)
    headingThirdErrAxe.set_ylabel("$Position\ Error(m)$", fontdict=firstFont)
    headingThirdErrAxe.set_title("$(f)$", fontdict=firstFont)
    headingThirdErrAxe.set_xlim(0, 60)
    headingThirdErrAxe.set_ylim(0, 14)
    headingThirdErrAxe.yaxis.set_major_locator(MultipleLocator(2))
    plt.xticks(fontsize=tickFontSize)
    plt.yticks(fontsize=tickFontSize)
    headingThirdErrAxe.grid(True)
    headingThirdErrAxe.legend(loc=2, fontsize=tickFontSize)

    plt.show()
    print("Done.")