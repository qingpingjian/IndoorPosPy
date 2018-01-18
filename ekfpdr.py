#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/1/18 14:46
@author: Pete
@email: yuwp_1985@163.com
@file: ekfpdr.py
@software: PyCharm Community Edition
"""

if __name__ == "__main__":
    sensorFilePath = ("./Examples/ExtendedKF/20180118102918_acce.csv", "./Examples/ExtendedKF/20180118102918_gyro.csv")
    wifiFilePath = "./Examples/ExtendedKF/20180118102918_wifi.csv"
    trainFileDir = "./RawData/RadioMap"
    locationFilePath = "./Examples/ExtendedKF/20180118102918_route.csv"
    pdrEstimateFilePath = "./Examples/ExtendedKF/20180118102918_estimate_pdr.csv"
    ekfEstimateFilePath = "./Examples/ExtendedKF/20180118102918_estimate_ekf.csv"
    # From local coordinate to global coordiante, they are related to route starting point and direction
    routeRotation = "270"
    moveVector = (39.3,10.4)

    # Load wifi radio map

    # Get the simple PDR estimations and related wifi estimations, then get the fusion based EFK
    # (1) Get the simple PDR estimations and transform to global coordinate

    # (2) realted wifi estimation

    # (3) fusion

    # (4) show the results

    print("Done.")