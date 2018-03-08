#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/3/1 22:32
@author: Pete
@email: yuwp_1985@163.com
@file: abstractmap.py
@software: PyCharm Community Edition
"""
"""
A <---> B <--> C <--> D <--> E <--> F <--> G
        T                                  H
        S                                  I
        R                                  |
Q <---> P <-> O <-> N <-> M <-> L <-> K <->J
"""

building1305 = {
    "nodes":{"seg1":(1.2, 1.7,  3.14159,  1.2, 10.7, 0.0), # (AB)
             "seg2":(1.2, 10.7, 3.14159,  1.2, 23.7, 0.0), # (BC)
             "seg3":(1.2, 23.7, 3.14159,  1.2, 41.3, 0.0), # (CD)
             "seg4":(1.2, 41.3, 3.14159,  1.2, 51.5, 0.0), # (DE)
             "seg5":(1.2, 51.5, 3.14159,  1.2, 60.95, 0.0), # (EF)
             "seg6":(1.2, 60.95,3.14159,  1.2, 78.05, 0.0), # (FG)
             "seg7":(1.2, 78.05,4.71239,  15.5, 78.05, 1.5708), # (GH)
             "seg8":(15.5,78.05,4.71239,  25.5, 78.05, 1.5708), # (HI)
             "seg9":(25.5,78.05,4.71239,  49.8, 78.05, 1.5708), # (IJ)
             "seg10":(49.8,59.15,3.14159, 49.8, 78.05, 0.0), # (KJ)
             "seg11":(49.8,41.15,3.14159, 49.8, 59.15, 0.0), # (LK)
             "seg12":(49.8,33.95,3.14159, 49.8, 41.15, 0.0), # (ML)
             "seg13":(49.8,24.95,3.14159, 49.8, 33.95, 0.0), # (NM)
             "seg14":(49.8,15.95,3.14159, 49.8, 24.95, 0.0), # (ON)
             "seg15":(49.8,10.7, 3.14159, 49.8, 15.95, 0.0), # (PO)
             "seg16":(49.8,1.95, 3.14159, 49.8, 10.7, 0.0), # (QP)
             "seg17":(37.5,10.7, 4.71239, 49.8, 10.7, 1.5708), # (RP)
             "seg18":(24.9,10.7, 4.71239, 37.5, 10.7, 1.5708), # (SR)
             "seg19":(15, 10.7, 4.71239,  24.9, 10.7, 1.5708), # (TS)
             "seg20":(1.2,10.7, 4.71239,  15, 10.7, 1.5708)},  # (BT)
    "edges": (("seg1", "seg1", 3),
              ("seg1", "seg1", 4),
              ("seg1", "seg2", 0, 1.2, 10.7),
              ("seg1", "seg20", 2, 1.2, 10.7),
              ("seg2", "seg2", 3),
              ("seg2", "seg2", 4),
              ("seg2", "seg1", 0, 1.2, 10.7),
              ("seg2", "seg3", 0, 1.2, 23.7),
              ("seg2", "seg20", 1, 1.2, 10.7),
              ("seg3", "seg3", 3),
              ("seg3", "seg3", 4),
              ("seg3", "seg2", 0, 1.2, 23.7),
              ("seg3", "seg4", 0, 1.2, 41.3),
              ("seg4", "seg4", 3),
              ("seg4", "seg4", 4),
              ("seg4", "seg3", 0, 1.2, 41.3),
              ("seg4", "seg5", 0, 1.2, 51.5),
              ("seg5", "seg5", 3),
              ("seg5", "seg5", 4),
              ("seg5", "seg4", 0, 1.2, 51.5),
              ("seg5", "seg6", 0, 1.2, 60.95),
              ("seg6", "seg6", 3),
              ("seg6", "seg6", 4),
              ("seg6", "seg5", 0, 1.2, 60.95),
              ("seg6", "seg7", 2, 1.2, 78.05),
              ("seg7", "seg7", 3),
              ("seg7", "seg7", 4),
              ("seg7", "seg6", 1, 1.2, 78.05),
              ("seg7", "seg8", 0, 15.5, 78.05),
              ("seg8", "seg8", 3),
              ("seg8", "seg8", 4),
              ("seg8", "seg7", 0, 15.5, 78.05),
              ("seg8", "seg9", 0, 25.5, 78.05),
              ("seg9", "seg9", 3),
              ("seg9", "seg9", 4),
              ("seg9", "seg8", 0, 25.5, 78.05),
              ("seg9", "seg10", 2, 49.8, 78.05),
              ("seg10", "seg10", 3),
              ("seg10", "seg10", 4),
              ("seg10", "seg9", 1, 49.8, 78.05),
              ("seg10", "seg11", 0, 49.8, 59.15),
              ("seg11", "seg11", 3),
              ("seg11", "seg11", 4),
              ("seg11", "seg10", 0, 49.8, 59.15),
              ("seg11", "seg12", 0, 49.8, 41.15),
              ("seg12", "seg12", 3),
              ("seg12", "seg12", 4),
              ("seg12", "seg11", 0, 49.8, 41.15),
              ("seg12", "seg13", 0, 49.8, 33.95),
              ("seg13", "seg13", 3),
              ("seg13", "seg13", 4),
              ("seg13", "seg12", 0, 49.8, 33.95),
              ("seg13", "seg14", 0, 49.8, 24.95),
              ("seg14", "seg14", 3),
              ("seg14", "seg14", 4),
              ("seg14", "seg13", 0, 49.8, 24.95),
              ("seg14", "seg15", 0, 49.8, 15.95),
              ("seg15", "seg15", 3),
              ("seg15", "seg15", 4),
              ("seg15", "seg14", 0, 49.8, 15.95),
              ("seg15", "seg16", 0, 49.8, 10.7),
              ("seg15", "seg17", 2, 49.8, 10.7),
              ("seg16", "seg16", 3),
              ("seg16", "seg16", 4),
              ("seg16", "seg15", 0, 49.8, 10.7),
              ("seg16", "seg17", 1, 49.8, 10.7),
              ("seg17", "seg17", 3),
              ("seg17", "seg17", 4),
              ("seg17", "seg15", 1, 49.8, 10.7),
              ("seg17", "seg16", 2, 49.8, 10.7),
              ("seg17", "seg18", 0, 37.5, 10.7),
              ("seg18", "seg18", 3),
              ("seg18", "seg18", 4),
              ("seg18", "seg17", 0, 37.5, 10.7),
              ("seg18", "seg19", 0, 24.9, 10.7),
              ("seg19", "seg19", 3),
              ("seg19", "seg19", 4),
              ("seg19", "seg18", 0, 24.9, 10.7),
              ("seg19", "seg20", 0, 15, 10.7),
              ("seg20", "seg20", 3),
              ("seg20", "seg20", 4),
              ("seg20", "seg19", 0, 15, 10.7),
              ("seg20", "seg1", 1, 1.2, 10.7),
              ("seg20", "seg2", 2, 1.2, 10.7)
              ),
}

import math
from anglefunc import angleNormalize, isHeadingMatch

class DigitalMap(object):
    def __init__(self, mapGraph=building1305):
        self.mapGraph = mapGraph
        self.nodesDict = mapGraph.get("nodes")
        self.edgesArray = mapGraph.get("edges")
        self.initProb = 1.0 # math.log(math.e)
        return

    def getSegmentLength(self, segIDArray):
        # TODO: Here, we donot check the segments are all in a straight narrow corridor
        length = 0.0
        # Try to sum all the length of input segments
        for segID in segIDArray:
            segAttr = self.nodesDict.get(segID)
            length = length + math.sqrt(math.pow(segAttr[0] - segAttr[3], 2) + math.pow(segAttr[1] - segAttr[4], 2))
        return length

    def extractSegmentByDir(self, walkingDir=0.0):
        normalWalkDir = angleNormalize(walkingDir)
        candidateList = []
        for id, attr in self.nodesDict.iteritems():
            firstAccessDir = attr[2]  # The accessible direction of the first endpoint
            secondAccessDir = attr[5]  # The accessible direction of the second endpoint
            if isHeadingMatch(normalWalkDir, firstAccessDir):
                # The second point is starting point and the first point is the next point
                candidateList.append([attr[3], attr[4], attr[0], attr[1], [id], self.initProb, self.initProb])
            elif isHeadingMatch(normalWalkDir, secondAccessDir):
                candidateList.append([attr[0], attr[1], attr[3], attr[4], [id], self.initProb, self.initProb])
        return candidateList


if __name__ == "__main__":
    print("Done.")