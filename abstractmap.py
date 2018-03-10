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
import numpy as np
import sys
from anglefunc import angleNormalize, isHeadingMatch

class DigitalMap(object):
    def __init__(self, mapGraph=building1305, logFlag=True):
        self.mapGraph = mapGraph
        self.nodesDict = mapGraph.get("nodes")
        self.edgesArray = mapGraph.get("edges")
        self.logFlag = logFlag
        self.initProb = -4.5 if logFlag else math.exp(-4.5)  # -4.5 = -1.0*(3delta)^2 / (2delta^2) about 0.0111
        self.minProb = -15.0 if logFlag else math.exp(-15)  # 3.059023205018258e-07
        return

    def isRelated(self, onePoint, otherPoint):
        """
        If it is reachable from onePoint to otherPoint through normal walking or another activities
        return true, otherwise, return false
        :param onePoint:  The end point of last segment
        :param otherPoint:  the start point of current segment
        :return:  True or False
        """
        return math.fabs(onePoint[0] - otherPoint[0]) < sys.float_info.epsilon and \
                math.fabs(onePoint[1] - otherPoint[1]) < sys.float_info.epsilon

    def isSamePoint(self, onePoint, otherPoint):
        return math.fabs(onePoint[0] - otherPoint[0]) < sys.float_info.epsilon and \
                math.fabs(onePoint[1] - otherPoint[1]) < sys.float_info.epsilon

    def getAnotherPoint(self, segID, onePoint):
        segAttr = self.nodesDict.get(segID)
        firstPoint = (segAttr[0], segAttr[1])
        secondPoint = (segAttr[3], segAttr[4])
        return secondPoint if self.isSamePoint(onePoint, firstPoint) else firstPoint

    def getHeadingDirection(self, segID, frontPoint):
        segAttr = self.nodesDict.get(segID)
        firstPoint = (segAttr[0], segAttr[1])
        return segAttr[2] if self.isSamePoint(frontPoint, firstPoint) else segAttr[5]

    def extendSegment(self, segID, endPoint):
        for edge in self.edgesArray:
            if len(edge) == 3:
                continue
            passedPoint = (edge[3], edge[4])
            if edge[0] == segID and edge[2] == 0 and self.isRelated(endPoint, passedPoint):
                return edge[1], self.getAnotherPoint(edge[1], passedPoint)

    def getSegmentLength(self, segIDArray):
        # TODO: Here, we donot check the segments are all in a straight narrow corridor
        length = 0.0
        # Try to sum all the length of input segments
        for segID in segIDArray:
            segAttr = self.nodesDict.get(segID)
            length = length + math.sqrt(math.pow(segAttr[0] - segAttr[3], 2) + math.pow(segAttr[1] - segAttr[4], 2))
        return length

    def extractSegmentByDir(self, walkingDir=0.0):
        """
        [startX, startY, endX, endY, ['s1', 's2', ..., 'sk'], probLastTime, probCurrent, pLastSegment, extendStatus]
        :param walkingDir: base direction to select segments candidate
        :return: segments candidate, the pLastProb is set to minProb firstly,
        and the extend status is set to zero, (0, 1, ..., possible counter num in a straight corridor)
        """
        normalWalkDir = angleNormalize(walkingDir)
        candidateList = []
        for id, attr in self.nodesDict.iteritems():
            firstAccessDir = attr[2]  # The accessible direction of the first endpoint
            secondAccessDir = attr[5]  # The accessible direction of the second endpoint
            if isHeadingMatch(normalWalkDir, firstAccessDir):
                # The second point is starting point and the first point is the next point
                candidateList.append([attr[3], attr[4], attr[0], attr[1], [id], self.initProb, self.initProb, self.minProb, 0])
            elif isHeadingMatch(normalWalkDir, secondAccessDir):
                candidateList.append([attr[0], attr[1], attr[3], attr[4], [id], self.initProb, self.initProb, self.minProb, 0])
        return candidateList

    def emissionProb(self, stepLength, stepNum, stepStd, segIDArray):
        travelDist = stepLength * stepNum
        distStd = stepStd * stepNum
        segLength = self.getSegmentLength(segIDArray)
        # TODO: the emission probability
        probValue = self.initProb
        if travelDist + 3 * distStd > segLength:
            probValue = math.exp((((travelDist - segLength) ** 2) / (2 * distStd ** 2)) * (-1.0))
            if self.logFlag:
                probValue = math.log(probValue)
        return probValue

    def nextCandidateByActivity(self, lastSeg, turnType, overPoint, currentProb):
        nextCandidate = None
        for edge in self.edgesArray:
            if edge[0] != lastSeg or edge[2] != turnType:
                continue
            if turnType == 3 or turnType == 4:  # turn around
                endPoint = self.getAnotherPoint(edge[1], overPoint)
                nextCandidate = [overPoint[0], overPoint[1], endPoint[0], endPoint[1], [edge[1]], self.initProb, self.initProb, currentProb, 0]
                break
            elif len(edge) == 5 and (turnType == 1 or turnType == 2): # left or right turn
                passedPoint = (edge[3], edge[4])
                if self.isRelated(overPoint, passedPoint):
                    endPoint = self.getAnotherPoint(edge[1], passedPoint)
                    nextCandidate = [passedPoint[0], passedPoint[1], endPoint[0], endPoint[1], [edge[1]], self.initProb, self.initProb, currentProb, 0]
                    break
        return nextCandidate

if __name__ == "__main__":
    # Emission Probability
    stepLength = 0.74
    stepStd = 0.1
    testMap = DigitalMap(logFlag=True)
    for segID, attr in testMap.nodesDict.iteritems():
        segLength = testMap.getSegmentLength([segID])
        probList = []
        for n in range(1, 40):
            probList.append(testMap.emissionProb(stepLength, n, stepStd, [segID]))
        # print segID,
        # print(probList)
        if probList[-1] <= testMap.minProb:
            print("Try to extend %s due to the current prob. %.5f" % (segID, probList[-1]))
    print("Done.")