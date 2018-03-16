#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/3/15 下午11:43
@author: Pete
@email: yuwp_1985@163.com
@file: jaccardwifi.py
@software: PyCharm Community Edition
"""

from dataloader import loadCrowdSourcedWifi

if __name__ == "__main__":
    wifiBoundDir = "./SegmentFingerprint/"
    radioMapDict = loadCrowdSourcedWifi(wifiBoundDir)
    # TODO: Second Trajectory of AiFiMatch
    print("Done.")