#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/3/8 11:04
@author: Pete
@email: yuwp_1985@163.com
@file: hmmmatching.py
@software: PyCharm Community Edition
"""
import matplotlib.pyplot as plt
import pandas as pd
import sys

from matplotlib.ticker import  MultipleLocator, FormatStrFormatter

from comutil import *
from abstractmap import *
from dataloader import loadAcceData, loadGyroData, loadMovingWifi
from wififunc import wifiDict2Str
from stepcounter import SimpleStepCounter
from turndetector import SimpleTurnDetector

class SegmentHMMMatcher(object):
    def __init__(self, personID="pete", logFlag=False):
        self.personID = personID
        self.matchStatus = "init" # "init", "mult", "covg"
        self.digitalMap = None
        self.radioMap = None
        self.viterbiList = None
        self.matchedSegmentSeq = None
        # bind wifi

        self.logFlag = logFlag
        return

    def updateDigitalMap(self, indoorMap):
        self.digitalMap = indoorMap

    def updateRadioMap(self, radioMap):
        self.radioMap = radioMap

    def checkSegment(self, stepLength, stepNum, stepStd, candidateList):
        """
        segment candidates List,
        [ [startX, startY, endX, endY, ['s1', 's2', ..., 'sk'], probLast, probCurrent, pLastBeforeActivity, extendNum],
        [startX, startY, endX, endY, ['s1', 's2', ..., 'sk'], probLast, probCurrent, pLastBeforeActivity, extendNum], ]
        if extendNum == 0， we can extend this candidate, if there is no segment, set to -1,
        otherwise set it to 1, add new candidate
        if extendNum == -1 and prob is low enough, we can filtered it out.
        if extendNum == 1 and prob is low enough, we can filtered it out
        :param : candidates array
        :return: filterd candidates array
        """
        # check the new prob of candidates unless there is only one segment left
        newCandidates = []
        # update probability for each segment candidate
        for candidate in candidateList:
            prob = self.digitalMap.emissionProb(stepLength, stepNum, stepStd, candidate[4])
            candidate[5] = candidate[6] # update the prob
            candidate[6] = prob

            # Maybe we can extend this segment
            travelDist = stepLength * stepNum
            travelDeviation = stepNum * stepStd
            segLength = self.digitalMap.getSegmentLength(candidate[4])
            if candidate[8] == 0 and travelDist + travelDeviation >= segLength and candidate[6] < candidate[5]:
                # Log information
                # print("Try to extend %s at step %d" % (candidate[4], stepNum))
                # Try to extend segment
                nextSegment = self.digitalMap.extendSegment(candidate[4][-1], (candidate[2], candidate[3]))
                if nextSegment == None: # The candidate can not extend
                    candidate[8] = -1
                else:
                    newSeg = nextSegment[0]
                    newEnd = nextSegment[1]
                    segIDArray = [segID for segID in candidate[4]]
                    segIDArray.append(newSeg)
                    newProb = self.digitalMap.emissionProb(stepLength, stepNum, stepStd, segIDArray)
                    # Now, we have find a new candidate and we need this candidate
                    candidate[8] = 1
                    newCandidate = [candidate[0], candidate[1], newEnd[0], newEnd[1], segIDArray, candidate[6], newProb, candidate[7], 0]
                    newCandidates.append(newCandidate)

        # There is only one candidate left
        newCandidates.extend(candidateList)
        if len(newCandidates) == 1:
            return newCandidates
        filteredCandidateList = []
        for candidate in newCandidates:
            if candidate[6] > self.digitalMap.minProb:
                filteredCandidateList.append(candidate)
        return filteredCandidateList

    def nextCandidate(self, turnType, candidateList):
        if self.logFlag:
            print(candidateList)
        # Now we meet a turn, then we should calcualte the most prob. segments based on turn types
        nextCandidateList = []
        for candidate in candidateList:
            nextCandidate = self.digitalMap.nextCandidateByActivity(candidate[4][-1], turnType, (candidate[2], candidate[3]), candidate[6])
            if nextCandidate != None:
                # TODO: get candidate by activity type, and we select the most probability segment and exclude others, is it right?
                hasDuplicate = False
                for newCandidate in nextCandidateList:
                    # different candidates chose the same next candidate, then we determine the most prob.
                    if newCandidate[4][0] == nextCandidate[4][0]:
                        hasDuplicate = True
                        newCandidate[7] = nextCandidate[7] if newCandidate[7] < nextCandidate[7] else newCandidate[7]
                        break
                if not hasDuplicate:
                    nextCandidateList.append(nextCandidate)
        # print("Num of next candidate is %d" % len(nextCandidateList))
        if self.logFlag:
            print(nextCandidateList)
        return nextCandidateList

    def onlineViterbi(self, acceTimeList, acceValueList,
                      gyroTimeList, gyroValueList,
                      wifiTimeList=None, wifiScanList=None,
                      startingDirection=0.0):
        self.matchStatus = "init"
        para = modelParameterDict.get(self.personID)

        # Count step
        acceValueArray = butterFilter(acceValueList)
        # Algorithm of step counter
        sc = SimpleStepCounter(self.personID)
        allIndexList = sc.countStep(acceTimeList, acceValueArray)
        stIndexList = allIndexList[0::3]
        stTimeList = [acceTimeList[i] for i in stIndexList]
        edIndexList = allIndexList[2::3]
        edTimeList = [acceTimeList[i] for i in edIndexList]
        stepNum = len(stIndexList)
        # Get step length
        stepFreq = stepNum / (edTimeList[-1] - stTimeList[0])
        stepLength = para[4] * stepFreq + para[5]
        print("Step Num is %d, Step Frequency is %.3f and Step Length is %.4f" % (stepNum, stepFreq, stepLength))
        self.stepLength = stepLength
        self.allStepIndexList = allIndexList

        # Detect Turns
        rotaValueList = rotationAngle(gyroTimeList, gyroValueList, normalize=False)
        rotaDegreeList = [r * 180.0 / math.pi for r in rotaValueList]
        windowSize = 23
        gyroTimeList, gyroValueList = slidingWindowFilter(gyroTimeList, gyroValueList, windowSize)
        simpleTd = SimpleTurnDetector(self.personID)
        turnIndexList, rtDegreeIndexList = simpleTd.detectTurn(gyroTimeList, gyroValueList, rotaDegreeList)
        # Turn point time and value
        turnTimeList = [gyroTimeList[i] for i in turnIndexList]
        turnValueList = [gyroValueList[i] for i in turnIndexList]
        rtTimeList = [gyroTimeList[i] for i in rtDegreeIndexList]
        rtValueList = [rotaDegreeList[i] for i in rtDegreeIndexList]
        edRtTimeList = rtTimeList[1::2]
        turnTypeList = []
        for i in range(0, len(rtTimeList), 2):
            turnTypeList.append(simpleTd.turnTranslate(rtValueList[i + 1] - rtValueList[i], humanFlag=False))
        self.turnTypeList = turnTypeList
        allTurnIndexList = []
        for i in range(len(turnIndexList)):
            allTurnIndexList.extend([rtDegreeIndexList[i*2], turnIndexList[i], rtDegreeIndexList[i*2+1]])
        self.allTurnIndexList = allTurnIndexList

        # Turn recognize and Step and Turn Alignment by time
        turnAtStepIndexList = []
        edStartIndex = 0
        for turnTime in turnTimeList:
            for edIndex in range(edStartIndex, len(edTimeList)):
                edt = edTimeList[edIndex]
                if edt > turnTime:
                    turnAtStepIndexList.append(edIndex)
                    edStartIndex = edIndex + 1
                    break
        #print(turnAtStepIndexList)
        endTurnAtStepIndexList = []
        edStartIndex = 0
        for edRt in edRtTimeList:
            for edIndex in range(edStartIndex, len(edTimeList)):
                edt = edTimeList[edIndex]
                if edt > edRt:
                    endTurnAtStepIndexList.append(edIndex)
                    edStartIndex = edIndex + 1
                    break
        #print(endTurnAtStepIndexList)
        for i in range(len(turnAtStepIndexList)):
            if turnAtStepIndexList[i] == endTurnAtStepIndexList[i]:
                endTurnAtStepIndexList[i] = turnAtStepIndexList[i] + 1

        # Reset the data storage of online viterbi algorithm
        self.onlineEstList = []
        self.viterbiList = []

        # Map Matching based on steps and turns
        # First, initial candidates from initial direction
        candidateList = self.digitalMap.extractSegmentByDir(startingDirection)
        print("The initial number of segment candidate is %d" % (len(candidateList)))
        # Initial point estimation
        initPoint = np.mean([(segment[0], segment[1]) for segment in candidateList], axis=0)
        print("The initial point estimation is (%.3f, %.3f)" % (initPoint[0], initPoint[1]))
        self.onlineEstList.append((initPoint[0], initPoint[1]))
        # TODO: give the initial point firstly, PDR should commit the previous line and uncommit the next line
        # self.onlineEstList.append((49.8, 1.95))
        if len(candidateList) > 1:
            self.matchStatus = "mult"
        elif len(candidateList) == 1:
            self.matchStatus = "covg"

        # Calculate the real directions for each step
        dirList = [r + startingDirection for r in rotaValueList]
        # Secondly, update locations for each step
        # 2.1
        stepDeviation = para[13] # step standard deviation
        currentTurnNum = 0
        currentGyroIndex = 0
        stepNumInSeg = 0
        for i in range(len(stIndexList)):
            asTime = stTimeList[i]
            aeTime = edTimeList[i]
            # If this is the end of some activity,
            # then, update segment candidate,
            # if i == endTurnAtStepIndexList[currentTurnNum] and False:
            if currentTurnNum < len(endTurnAtStepIndexList) and i == endTurnAtStepIndexList[currentTurnNum]:
                self.viterbiList.append(candidateList)
                # Now, we should have a new segment candidate list
                candidateList = self.nextCandidate(turnTypeList[currentTurnNum], candidateList)
                # Check and update the new candidates
                j = turnAtStepIndexList[currentTurnNum]
                stepNumInSeg = i - j # Have walked i-j steps after turning
                candidateList = self.checkSegment(stepLength, stepNumInSeg, stepDeviation, candidateList)
                # update the matching status
                if (len(candidateList) == 1):
                    self.matchStatus = "covg"
                else:
                    self.matchStatus = "mult"
                rotStartIndex = timeAlign(asTime, gyroTimeList, currentGyroIndex)
                currentGyroIndex = rotStartIndex - 1
                rotEndIndex = timeAlign(aeTime, gyroTimeList, currentGyroIndex)
                currentGyroIndex = rotEndIndex - 1
                # The direction and starting point updation
                if self.matchStatus == "covg":  # loccation estimation and direction
                    # update heading direction
                    headingBasedSeg =self.digitalMap.getHeadingDirection(candidateList[0][4][-1], (candidateList[0][2], candidateList[0][3]))
                    dirList = [angleNormalize(dir - dirList[rotEndIndex] + headingBasedSeg) for dir in dirList]
                    direction = dirList[rotEndIndex]  # This direction should equal to headingBasedSeg
                    if (turnTypeList[currentTurnNum] > 2):  # Turn around activity can not get the turn points, then we used the pdr one
                        lastLoc = self.onlineEstList[-1]
                        xLoc = lastLoc[0] + stepLength * math.sin(direction)
                        yLoc = lastLoc[1] + stepLength * math.cos(direction)
                        self.onlineEstList.append((xLoc, yLoc))
                    else:  # we suppose that the direction should not change after turnning.
                        passedPoint = (candidateList[0][0], candidateList[0][1])
                        xLoc = passedPoint[0] + stepNumInSeg * stepLength * math.sin(direction)
                        yLoc = passedPoint[1] + stepNumInSeg * stepLength * math.cos(direction)
                        self.onlineEstList.append((xLoc, yLoc))
                else: # update location estimation by new candidates starting points
                    if self.logFlag:
                        print("The number candidate now is %d" % len(candidateList))
                    turnPoints = np.mean([(segment[0], segment[1]) for segment in candidateList], axis=0)
                    newHeading = meanAngle([self.digitalMap.getHeadingDirection(candidate[4][-1], (candidate[2], candidate[3]))
                                            for candidate in candidateList], normalize=True)
                    # print(turnPoints)
                    # print(newHeading)
                    xLoc = float(turnPoints[0]) + stepNumInSeg * stepLength * math.sin(newHeading)
                    yLoc = float(turnPoints[1]) + stepNumInSeg * stepLength * math.cos(newHeading)
                    self.onlineEstList.append((xLoc, yLoc))
                # Ready to the next activity
                currentTurnNum = currentTurnNum + 1
            else:
                # update candidates prob.
                stepNumInSeg = stepNumInSeg + 1
                candidateList = self.checkSegment(stepLength, stepNumInSeg, stepDeviation, candidateList)
                if len(candidateList) == 1:
                    self.matchStatus = "covg"
                rotStartIndex = timeAlign(asTime, gyroTimeList, currentGyroIndex)
                currentGyroIndex = rotStartIndex - 1
                rotEndIndex = timeAlign(aeTime, gyroTimeList, currentGyroIndex)
                currentGyroIndex = rotEndIndex - 1
                direction = meanAngle(dirList[rotStartIndex:rotEndIndex + 1])
                lastLoc = self.onlineEstList[-1]
                xLoc = lastLoc[0] + stepLength * math.sin(direction)
                yLoc = lastLoc[1] + stepLength * math.cos(direction)
                self.onlineEstList.append((xLoc, yLoc))
        self.viterbiList.append(candidateList)
        self.getSegmentSequence()
        return

    def getSegmentSequence(self):
        self.matchedSegmentSeq = None
        if self.viterbiList == None or self.matchStatus != "covg":
            return
        self.matchedSegmentSeq = []
        self.matchedSegmentSeq.append(self.viterbiList[-1][0][4])
        currentStart = (self.viterbiList[-1][0][0], self.viterbiList[-1][0][1])
        lastProb = self.viterbiList[-1][0][7]
        for cIndex in range(len(self.viterbiList) - 2, -1, -1):
            if self.logFlag and len(self.matchedSegmentSeq) + cIndex != len(self.viterbiList) - 1:
                print("Don't find the matched segments, there must be something wrong happened: message %d" % (cIndex))
                break
            candidateList = self.viterbiList[cIndex]
            for candidate in candidateList:
                endPoint = (candidate[2], candidate[3])
                candidateProb = candidate[6]
                if self.digitalMap.isRelated(currentStart, endPoint) and math.fabs(lastProb - candidateProb) <= sys.float_info.epsilon:
                    self.matchedSegmentSeq.append(candidate[4])
                    currentStart = (candidate[0], candidate[1])
                    lastProb = candidate[7]
                    break
        self.matchedSegmentSeq.reverse()
        if self.logFlag:
            print(self.matchedSegmentSeq)
        return

    def bindWiFi(self, acceTimeList, gyroTimeList, wifiTimeList, wifiScanList):
        if self.matchedSegmentSeq == None:
            return
        peakIndexList = self.allStepIndexList[1::3]
        peakTimeList = [acceTimeList[i] for i in peakIndexList]
        endIndexList = self.allStepIndexList[2::3]
        endTimeList = [acceTimeList[i] for i in endIndexList]

        turnStartIndexList = self.allTurnIndexList[0::3]
        turnStartTimeList = [gyroTimeList[i] for i in turnStartIndexList]
        turnIndexList = self.allTurnIndexList[1::3]
        turnTimeList = [gyroTimeList[i] for i in turnIndexList]
        turnEndIndexList = self.allTurnIndexList[2::3]
        turnEndTimeList = [gyroTimeList[i] for i in turnEndIndexList]

        tsIndexList, stsIndexList, etsIndexList = turnAlignStep(endTimeList, turnStartTimeList, turnTimeList, turnEndTimeList)
        currentWifiIndex = 0
        wifiBoundList = []
        for i in range(0, len(self.turnTypeList)-1):
            if self.turnTypeList[i] < 3 and self.turnTypeList[i+1] < 3:
                print("%d turn and %d next turn is satisfied" % (i, i+1))
                # Get the transition point
                segmentIDArray = self.matchedSegmentSeq[i+1]
                firstPoint = self.digitalMap.getSegmentSeparatePoint(self.matchedSegmentSeq[i][-1], self.matchedSegmentSeq[i+1][0])
                secondPoint = self.digitalMap.getSegmentSeparatePoint(self.matchedSegmentSeq[i+1][-1], self.matchedSegmentSeq[i+2][0])
                firstStepIndex = tsIndexList[i]
                secondStepIndex = tsIndexList[i+1]
                offlineLocList = genLocation(firstPoint, secondPoint, secondStepIndex-firstStepIndex)
                for stepIndex in range(firstStepIndex, secondStepIndex+1):
                    startWifiTime = peakTimeList[stepIndex]
                    endWifiTime = peakTimeList[stepIndex + 1]
                    currentWifiIndex, currentWifiDict = wifiExtract(startWifiTime, endWifiTime, wifiTimeList, wifiScanList,
                                                                    currentWifiIndex)
                    if currentWifiDict != None:
                        offlineLoc = offlineLocList[stepIndex-firstStepIndex]
                        segBound = self.digitalMap.selectSegment(offlineLoc, segmentIDArray)
                        wifiBoundList.append((segBound,
                                              round(offlineLoc[0] * 1000) / 1000,
                                              round(offlineLoc[1] * 1000) / 1000,
                                              wifiDict2Str(currentWifiDict)))
        return wifiBoundList


if __name__ == "__main__":
    sensorFilePath = ("./RawData/AiFiMatch/ThirdTrajectory/20180303143913_acce.csv",
                      "./RawData/AiFiMatch/ThirdTrajectory/20180303143913_gyro.csv",
                      "./RawData/AiFiMatch/ThirdTrajectory/20180303143913_wifi.csv")
    locationFilePath = "./RawData/AiFiMatch/ThirdTrajectory/20180303143913_route.csv"
    estimationFilePath = "./RawData/AiFiMatch/ThirdTrajectory/20180303143913_estimate_aifi_online.csv"
    # Load sensor data from files
    acceTimeList, acceValueList = loadAcceData(sensorFilePath[0], relativeTime=False)
    gyroTimeList, gyroValueList = loadGyroData(sensorFilePath[1], relativeTime=False)
    wifiTimeList, wifiScanList = loadMovingWifi(sensorFilePath[2])

    firstMatcher = SegmentHMMMatcher(logFlag=False)
    myDigitalMap = DigitalMap()
    firstMatcher.updateDigitalMap(myDigitalMap)

    initDirection = 0.0
    firstMatcher.onlineViterbi(acceTimeList, acceValueList, gyroTimeList, gyroValueList)

    # Bin wifi fingerprint
    wifiBoundList = firstMatcher.bindWiFi(acceTimeList, gyroTimeList, wifiTimeList, wifiScanList)
    wifiBoundDF = pd.DataFrame(np.array(wifiBoundList), columns=["segid", "coordx", "coordy", "wifiinfos"])
    wifiBoundFilePath = "%s_bind.csv" % sensorFilePath[2][0:-4]
    wifiBoundDF.to_csv(wifiBoundFilePath, encoding="utf-8", index=False)
    print(wifiBoundFilePath)


    # Save the estimate locations
    locEstList = [(round(loc[0] * 1000) / 1000, round(loc[1] * 1000) / 1000) for loc in firstMatcher.onlineEstList]
    locEstDF = pd.DataFrame(np.array(locEstList), columns=["EX(m)", "EY(m)"])
    locEstDF.to_csv(estimationFilePath, encoding='utf-8', index=False)

    # load real locations
    locRealDF = pd.read_csv(locationFilePath)

    # Calculate the location errors
    locRealList = [(loc[0], loc[1]) for loc in locRealDF.values]
    errorList = distError(locRealList, locEstList)

    # Save the errors
    errorList = [round(err * 1000) / 1000 for err in errorList]
    errorFilePath = "%s_error_aifi_online.csv" % locationFilePath[0:-4]
    errorDF = pd.DataFrame(np.array(errorList), columns=["Error(m)"])
    errorDF.to_csv(errorFilePath, encoding='utf-8', index=False)

    print("Average Error Distance is %.3f" % np.mean(errorList))

    # Show the errors
    pdrxMajorLocator = MultipleLocator(40)
    pdrxMajorFormatter = FormatStrFormatter("%d")
    pdrxMinorLocator = MultipleLocator(20)
    pdryMajorLocator = MultipleLocator(1.0)
    pdryMajorFormatter = FormatStrFormatter("%.1f")
    pdryMinorLocator = MultipleLocator(0.5)

    fig = plt.figure()
    pdrAxe = fig.add_subplot(111)

    pdrAxe.xaxis.set_major_locator(pdrxMajorLocator)
    pdrAxe.xaxis.set_major_formatter(pdrxMajorFormatter)
    pdrAxe.xaxis.set_minor_locator(pdrxMinorLocator)
    pdrAxe.yaxis.set_major_locator(pdryMajorLocator)
    pdrAxe.yaxis.set_major_formatter(pdryMajorFormatter)
    pdrAxe.yaxis.set_minor_locator(pdryMinorLocator)
    pdrAxe.set_xlabel("$Step\ Number$")
    pdrAxe.set_ylabel("$Position\ Error(m)$")
    pdrAxe.plot(range(len(errorList)), errorList, color="r", lw=2, label="PDR")
    plt.legend(loc=2)
    plt.grid()
    #plt.show()
    print("Done.")