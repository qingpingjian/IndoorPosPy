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
    stepT1ErrorFile = "pdr_error_step_t1_0515.csv"
    stepT2ErrorFile = "pdr_error_step_t2_0515.csv"
    stepT3ErrorFile = "pdr_error_step_t3_0515.csv"

    headingT1ErrorFile = "pdr_error_heading_t1_0515.csv"
    headingT2ErrorFile = "pdr_error_heading_t2_0515.csv"
    headingT3ErrorFile = "pdr_error_heading_t3_0515.csv"

    # Step Length Error
    stepT1ErrorDF = pd.read_csv(stepT1ErrorFile)
    stepT1ErrorArray = stepT1ErrorDF.ix[1:, ["Delta_Step", "Error(m)"]].values
    stepT2ErrorDF = pd.read_csv(stepT2ErrorFile)
    stepT2ErrorArray = stepT2ErrorDF.ix[1:, ["Delta_Step", "Error(m)"]].values
    stepT3ErrorDF = pd.read_csv(stepT3ErrorFile)
    stepT3ErrorArray = stepT3ErrorDF.ix[1:, ["Delta_Step", "Error(m)"]].values

    # Heading Error
    headingT1ErrorDF = pd.read_csv(headingT1ErrorFile)
    headingT1ErrArray = headingT1ErrorDF.ix[1:, ["Delta_Heading", "Error(m)"]].values
    headingT2ErrorDF = pd.read_csv(headingT2ErrorFile)
    headingT2ErrArray = headingT2ErrorDF.ix[1:, ["Delta_Heading", "Error(m)"]].values
    headingT3ErrorDF = pd.read_csv(headingT3ErrorFile)
    headingT3ErrorArray = headingT3ErrorDF.ix[1:, ["Delta_Heading", "Error(m)"]].values

    # Plot the axes
    fig = plt.figure()
    stepFirstErrAxe = plt.subplot(231)
    stepFirstErrAxe.plot(stepT1ErrorArray[:, 0], stepT1ErrorArray[:, 1], "r-", marker="^", linewidth=2, label="$Basic\ PDR$")
    stepFirstErrAxe.set_xlabel("$\sigma_d(m)$", fontdict=firstFont)
    stepFirstErrAxe.set_ylabel("$Position\ Error(m)$", fontdict=firstFont)
    stepFirstErrAxe.set_xlim(0.0, 0.6)
    stepFirstErrAxe.set_ylim(2, 8)
    stepFirstErrAxe.yaxis.set_major_locator(MultipleLocator(2))
    stepFirstErrAxe.yaxis.set_minor_locator(MultipleLocator(1))
    plt.xticks(fontsize=tickFontSize)
    plt.yticks(fontsize=tickFontSize)
    stepFirstErrAxe.grid(True)
    stepFirstErrAxe.legend(loc=2, fontsize=tickFontSize)

    stepSecondErrAxe = plt.subplot(232)
    stepSecondErrAxe.plot(stepT2ErrorArray[:, 0], stepT2ErrorArray[:, 1], "r-", marker="^", linewidth=2, label="$Basic\ PDR$")
    stepSecondErrAxe.set_xlabel("$\sigma_d(m)$", fontdict=firstFont)
    stepSecondErrAxe.set_ylabel("$Position\ Error(m)$", fontdict=firstFont)
    stepSecondErrAxe.set_xlim(0.0, 0.6)
    stepSecondErrAxe.set_ylim(2, 6)
    stepSecondErrAxe.yaxis.set_major_locator(MultipleLocator(2))
    stepSecondErrAxe.yaxis.set_minor_locator(MultipleLocator(1))
    plt.xticks(fontsize=tickFontSize)
    plt.yticks(fontsize=tickFontSize)
    stepSecondErrAxe.grid(True)
    stepSecondErrAxe.legend(loc=2, fontsize=tickFontSize)

    stepThirdErrAxe = plt.subplot(233)
    stepThirdErrAxe.plot(stepT3ErrorArray[:, 0], stepT3ErrorArray[:, 1], "r-", marker="^", linewidth=2, label="$Basic\ PDR$")
    stepThirdErrAxe.set_xlabel("$\sigma_d(m)$", fontdict=firstFont)
    stepThirdErrAxe.set_ylabel("$Position\ Error(m)$", fontdict=firstFont)
    stepThirdErrAxe.set_xlim(0.0, 0.6)
    stepThirdErrAxe.set_ylim(2, 6)
    stepThirdErrAxe.yaxis.set_major_locator(MultipleLocator(2))
    stepThirdErrAxe.yaxis.set_minor_locator(MultipleLocator(1))
    plt.xticks(fontsize=tickFontSize)
    plt.yticks(fontsize=tickFontSize)
    stepThirdErrAxe.grid(True)
    stepThirdErrAxe.legend(loc=2, fontsize=tickFontSize)

    headingFirstErrAxe = plt.subplot(234)
    headingFirstErrAxe.plot(headingT1ErrArray[:, 0], headingT1ErrArray[:, 1], "r-", marker="^", linewidth=2, label="$Basic\ PDR$")
    headingFirstErrAxe.set_xlabel(r"$\sigma_{\varphi}(degree)$", fontdict=firstFont)
    headingFirstErrAxe.set_ylabel("$Position\ Error(m)$", fontdict=firstFont)
    headingFirstErrAxe.set_xlim(0, 60)
    headingFirstErrAxe.set_ylim(2, 14)
    headingFirstErrAxe.yaxis.set_major_locator(MultipleLocator(2))
    plt.xticks(fontsize=tickFontSize)
    plt.yticks(fontsize=tickFontSize)
    headingFirstErrAxe.grid(True)
    headingFirstErrAxe.legend(loc=2, fontsize=tickFontSize)

    headingSecondErrAxe = plt.subplot(235)
    headingSecondErrAxe.plot(headingT2ErrArray[:, 0], headingT2ErrArray[:, 1], "r-", marker="^", linewidth=2, label="$Basic\ PDR$")
    headingSecondErrAxe.set_xlabel(r"$\sigma_{\varphi}(degree)$", fontdict=firstFont)
    headingSecondErrAxe.set_ylabel("$Position\ Error(m)$", fontdict=firstFont)
    headingSecondErrAxe.set_xlim(0, 60)
    headingSecondErrAxe.set_ylim(2, 14)
    headingSecondErrAxe.yaxis.set_major_locator(MultipleLocator(2))
    plt.xticks(fontsize=tickFontSize)
    plt.yticks(fontsize=tickFontSize)
    headingSecondErrAxe.grid(True)
    headingSecondErrAxe.legend(loc=2, fontsize=tickFontSize)

    headingThirdErrAxe = plt.subplot(236)
    headingThirdErrAxe.plot(headingT3ErrorArray[:, 0], headingT3ErrorArray[:, 1], "r-", marker="^", linewidth=2, label="$Basic\ PDR$")
    headingThirdErrAxe.set_xlabel(r"$\sigma_{\varphi}(degree)$", fontdict=firstFont)
    headingThirdErrAxe.set_ylabel("$Position\ Error(m)$", fontdict=firstFont)
    headingThirdErrAxe.set_xlim(0, 60)
    headingThirdErrAxe.set_ylim(2, 14)
    headingThirdErrAxe.yaxis.set_major_locator(MultipleLocator(2))
    plt.xticks(fontsize=tickFontSize)
    plt.yticks(fontsize=tickFontSize)
    headingThirdErrAxe.grid(True)
    headingThirdErrAxe.legend(loc=2, fontsize=tickFontSize)

    plt.show()
    print("Done.")