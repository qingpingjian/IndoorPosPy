#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/1/19 10:40
@author: Pete
@email: yuwp_1985@163.com
@file: ekfmodel.py
@software: PyCharm Community Edition
"""
import math
import numpy as np

class ExtendedKF(object):
    def __init__(self, initState, processCov, observeTransfer, observeCov):
        """
        :param initState: (0.0, init_X, init_Y)
        :param processCov: (headingVar, xVar, yVar)
        :param observeTransfer: [[0,1,0],[0,0,1]]
        :param observeCov: (ZxVar,ZyVar)
        """
        self.dimState = len(initState)
        self.estimate = initState
        self.previousEstimate = initState
        self.Q = processCov  # process noise covariance
        self.arg = None # Record step length

        self.P = np.identity(self.dimState)
        self.previousP = np.identity(self.dimState)

        self.H = observeTransfer
        self.R = observeCov
        self.gain = np.dot(np.identity(self.dimState), np.transpose(observeTransfer))

    def sateTransferFunc(self, stepLen, headingState):
        s = self.previousEstimate
        xLoc = float(s[1][0]) + stepLen * math.sin(headingState)
        yLoc = float(s[2][0]) + stepLen * math.cos(headingState)
        return np.matrix([[headingState], [xLoc], [yLoc]])

    def stateJac(self):
        stepLeng = self.arg
        headingDirect = float(self.estimate[0][0])
        fMat = np.identity(self.dimState)
        fMat[1][0] = stepLeng * math.cos(headingDirect)
        fMat[2][0] = stepLeng * (-1.0) * math.sin(headingDirect)
        return fMat

    def predict(self, stepLen, headingState):
        """
        Called first.
        Predicts estimate and error prediction according to model of the situation
        """
        # find the jacobian value
        if self.arg == None:
            self.arg = stepLen
        jacVal = self.stateJac()

        # update current state
        self.estimate = self.sateTransferFunc(stepLen, headingState)
        # Remember the step length
        self.arg = stepLen

        # update error prediction state
        self.P = np.dot(jacVal, np.dot(self.previousP, np.transpose(jacVal))) + self.Q

    def update(self, currentObservation):
        """
        Called second.
        Updates estimate according to combination of observed and prediction.
        Also updates our learning parameters of gain and error prediction.
        """
        # update the gain
        invVal = np.dot(self.H, np.dot(self.P, np.transpose(self.H))) + self.R # 2*2
        self.gain = np.dot(self.P, np.dot(np.transpose(self.H), np.linalg.inv(invVal)))

        # update the current estimate based on the gain
        self.estimate = self.estimate + np.dot(self.gain, (currentObservation - np.dot(self.H, self.estimate)))

        # update error prediction
        self.P = np.dot((np.identity(self.dimState) - np.dot(self.gain, self.H)), self.P)

        # update variables for next round
        self.previousEstimate = self.estimate
        self.previousP = self.P

    def getEstLocation(self):
        """
        Simple getter for state estimation,
        prior state value after predict and posterior state value after update
        """
        return (self.estimate[1][0], self.estimate[2][0])


if __name__ == "__main__":
    print("Done.")