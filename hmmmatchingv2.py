#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/5/15 22:22
@author: Pete
@email: yuwp_1985@163.com
@file: hmmmatchingv2.py.py
@software: PyCharm Community Edition
"""
import pandas as pd
import random as rd
import time

from comutil import *
from abstractmap import *
from dataloader import loadAcceData, loadGyroData, loadMovingWifi
from stepcounter import SimpleStepCounter
from turndetector import SimpleTurnDetector

class AiFiMatcher(object):
    def __init__(self, personID="pete"):
        self.personID = personID
        return

    def updateDigitalMap(self, indoorMap):
        self.digitalMap = indoorMap

    def updateRadioMap(self, radioMap):
        self.radioMap = radioMap

    # Just for testing heading errors
    def gyroIndexByTime(self, turnTimeList, gyroTimeList):
        gyroIndexList = []
        currentGyroIndex = 0
        for turnTime in turnTimeList:
            gIndex = timeAlign(turnTime, gyroTimeList, currentGyroIndex)
            currentGyroIndex = gIndex + 1
            gyroIndexList.append(gIndex)
        return gyroIndexList

    def nextCandidate(self, turnType, candidateList, debugFlag=False):
        if debugFlag:
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
        if debugFlag:
            print(nextCandidateList)
        return nextCandidateList

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
        if stepStd < 0.00001:
            stepStd = 0.05
        # check the new prob of candidates unless there is only one segment left
        newCandidates = []
        # update probability for each segment candidate
        for candidate in candidateList:
            prob = self.digitalMap.emissionProb(stepLength, stepNum, stepStd, candidate[4])
            candidate[5] = candidate[6]  # update the prob
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
                if nextSegment == None:  # The candidate can not extend
                    candidate[8] = -1
                else:
                    newSeg = nextSegment[0]
                    newEnd = nextSegment[1]
                    segIDArray = [segID for segID in candidate[4]]
                    segIDArray.append(newSeg)
                    newProb = self.digitalMap.emissionProb(stepLength, stepNum, stepStd, segIDArray)
                    # Now, we have find a new candidate and we need this candidate
                    candidate[8] = 1
                    newCandidate = [candidate[0], candidate[1], newEnd[0], newEnd[1], segIDArray, candidate[6], newProb,
                                    candidate[7], 0]
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

    def onlineViterbi(self, acceTimeList, acceValueList,
                      gyroTimeList, gyroValueList,
                      wifiTimeList=None, wifiScanList=None,
                      startingDirection=0.0, # In radian
                      startingPointFlag=True,
                      startingPoint=(0.0, 0.0),
                      stepError=0,
                      headingError=0):
        para = modelParameterDict.get(self.personID)
        # ***** -- Count step -- ***** #
        acceValueArray = butterFilter(acceValueList)
        # Algorithm of step counter
        sc = SimpleStepCounter(self.personID)
        allIndexList = sc.countStep(acceTimeList, acceValueArray)
        stIndexList = allIndexList[0::3]
        stTimeList = [acceTimeList[i] for i in stIndexList]
        edIndexList = allIndexList[2::3]
        edTimeList = [acceTimeList[i] for i in edIndexList]
        stepNum = len(stIndexList)

        # ***** -- Get step length -- ***** #
        stepFreq = stepNum / (edTimeList[-1] - stTimeList[0])
        stepLengthRegress = para[4] * stepFreq + para[5]
        stepDeviation = stepError # Standard deviation of step length

        # print("Step Num is %d, Step Frequency is %.3f and Step Length is %.4f" % (stepNum, stepFreq, stepLengthRegress))

        # ***** -- Detect Turns -- ***** #
        rotaValueList = rotationAngle(gyroTimeList, gyroValueList, normalize=False)
        # Adding gaussian error to rotation values
        # degree to radian
        headingErrorInRad = headingError * (math.pi / 180.0)
        rotaValueList = [r + rd.gauss(0, headingErrorInRad) for r in rotaValueList]
        rotaDegreeList = [r * 180.0 / math.pi for r in rotaValueList] # Radian to Degree
        windowSize = 23
        gyroTimeList, gyroValueList = slidingWindowFilter(gyroTimeList, gyroValueList, windowSize)
        simpleTd = SimpleTurnDetector(self.personID)
        allTurnIndexList = simpleTd.detectTurnV2(gyroTimeList, gyroValueList, rotaDegreeList)
        turnPointIndexList = allTurnIndexList[1::3]
        turnTimeList = [gyroTimeList[i] for i in turnPointIndexList]
        turnPointStepIndexList = turnAlignStepByTime(turnTimeList, edTimeList)
        turnStartStepIndexList = [sIndex - 2 for sIndex in turnPointStepIndexList]
        turnStartBaseTimeList = [edTimeList[sIndex] for sIndex in turnStartStepIndexList]
        turnStartIndexList = self.gyroIndexByTime(turnStartBaseTimeList, gyroTimeList)
        turnStartValueList = [rotaDegreeList[i] for i in turnStartIndexList]
        turnEndStepIndexList = [sIndex + 2 for sIndex in turnPointStepIndexList]
        turnEndBaseTimeList = [edTimeList[sIndex] for sIndex in turnEndStepIndexList]
        turnEndIndexList = self.gyroIndexByTime(turnEndBaseTimeList, gyroTimeList)
        turnEndValueList = [rotaDegreeList[i] for i in turnEndIndexList]

        turnTypeList = []
        for i in range(len(turnPointIndexList)):
            turnTypeList.append(simpleTd.turnTranslate(turnEndValueList[i] - turnStartValueList[i], humanFlag=False))
        # print turnTypeList

        # Calculate the real directions for each step
        headingList = [r + startingDirection for r in rotaValueList]

        # TODO: Notice that the starting point is already known.
        # Get CandidateList according to starting point and heading direction
        candidateList = self.digitalMap.extractSegmentByDirAndStartPoint(startingDirection)
        matchStatus = "covg"
        # print candidateList

        estiLocList = [startingPoint] if startingPointFlag else [(0, 0)]
        currentTurnIndex = 0
        currentGyroIndex = 0
        stepNumInSeg = 0
        for i in range(len(stIndexList)):
            asTime = stTimeList[i]
            aeTime = edTimeList[i]
            # Step length with gaussian errors
            stepLength = stepLengthRegress + rd.gauss(0, stepError)
            if currentTurnIndex < len(turnTypeList) and i == turnEndStepIndexList[currentTurnIndex]: # Find a turn
                # Now, we should have a new segment candidate list
                candidateList = self.nextCandidate(turnTypeList[currentTurnIndex], candidateList)
                # Check and update the new candidates
                j = turnPointStepIndexList[currentTurnIndex]
                stepNumInSeg = i - j # Have walked i-j steps after turning
                candidateList = self.checkSegment(stepLengthRegress, stepNumInSeg, stepDeviation, candidateList)
                # update the matching status
                if (len(candidateList) == 1):
                    matchStatus = "covg"
                else:
                    matchStatus = "mult"
                rotStartIndex = timeAlign(asTime, gyroTimeList, currentGyroIndex)
                currentGyroIndex = rotStartIndex - 1
                rotEndIndex = timeAlign(aeTime, gyroTimeList, currentGyroIndex)
                currentGyroIndex = rotEndIndex - 1
                # The direction and starting point updation
                if matchStatus == "covg":  # loccation estimation and direction
                    # update heading direction
                    headingBasedSeg =self.digitalMap.getDirection(candidateList[0][4][-1], (candidateList[0][2], candidateList[0][3]))
                    headingList = [angleNormalize(dir - headingList[rotEndIndex] + headingBasedSeg) for dir in headingList]
                    direction = headingList[rotEndIndex]  # This direction should equal to headingBasedSeg
                    if (turnTypeList[currentTurnIndex] > 2):  # Turn around activity can not get the turn points, then we used the pdr one
                        lastLoc = estiLocList[-1]
                        xLoc = lastLoc[0] + stepLength * math.sin(direction)
                        yLoc = lastLoc[1] + stepLength * math.cos(direction)
                        estiLocList.append((xLoc, yLoc))
                    else:  # we suppose that the direction should not change after turning.
                        passedPoint = (candidateList[0][0], candidateList[0][1])
                        xLoc = passedPoint[0] + stepNumInSeg * stepLength * math.sin(direction)
                        yLoc = passedPoint[1] + stepNumInSeg * stepLength * math.cos(direction)
                        estiLocList.append((xLoc, yLoc))
                else: # we uses the PDR data
                    currentHeading = meanAngle(headingList[rotStartIndex:rotEndIndex + 1])
                    lastLoc = estiLocList[-1]
                    xLoc = lastLoc[0] + stepLength * math.sin(currentHeading)
                    yLoc = lastLoc[1] + stepLength * math.cos(currentHeading)
                    estiLocList.append((xLoc, yLoc))
                currentTurnIndex += 1
            else:
                # ***** -- update candidates prob. -- ***** #
                stepNumInSeg += 1
                candidateList = self.checkSegment(stepLengthRegress, stepNumInSeg, stepDeviation, candidateList)
                # if len(candidateList) == 1:
                #     matchStatus = "covg"
                rotStartIndex = timeAlign(asTime, gyroTimeList, currentGyroIndex)
                currentGyroIndex = rotStartIndex - 1
                rotEndIndex = timeAlign(aeTime, gyroTimeList, currentGyroIndex)
                currentGyroIndex = rotEndIndex - 1
                currentHeading = meanAngle(headingList[rotStartIndex:rotEndIndex + 1])
                lastLoc = estiLocList[-1]
                xLoc = lastLoc[0] + stepLength * math.sin(currentHeading)
                yLoc = lastLoc[1] + stepLength * math.cos(currentHeading)
                estiLocList.append((xLoc, yLoc))
        return estiLocList


if __name__ == "__main__":
    # TODO: ***** -- ***** #
    controlFlag = 1 # 0 : Testing Demo, 1 : AiFiMatch
    showFlags = (True, True, False, False)
    secondAiFi = AiFiMatcher()
    myDigitalMap = DigitalMap()
    secondAiFi.updateDigitalMap(myDigitalMap)
    if controlFlag == 0:
        pass
    elif controlFlag == 1:
        # TODO: *****-- ***** #
        # Performance VS. Step Length Error
        stepLengthErrorList = (0.0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5)
        headingErrorList = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        errorType = "step"
        # Performance VS. Heading Error
        # stepLengthErrorList = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        # headingErrorList = (0, 10, 15, 20, 25, 30, 35, 40, 45, 50)
        # errorType = "heading"

        rawDataArray = []
        # initial point and direction
        routeRotClockWise = "0"
        moveVector = (1.2, 1.7)
        # TODO: *****-- ***** #
        saveFlags = (False, False, False) # From 0 index
        rootDirectory = "./RawData/AiFiMatch/ErrorInfluence"
        dataBelongs = "t1"
        # TODO: *****-- ***** #
        trajectorySwitch = 3
        if trajectorySwitch == 1:
            # TODO: First trajectory of AiFiMatch
            rawDataArrayofFirst = [
                # (# The first one
                #     "./RawData/AiFiMatch/FirstTrajectory/20180302213401_acce.csv",
                #     "./RawData/AiFiMatch/FirstTrajectory/20180302213401_gyro.csv",
                #     "./RawData/AiFiMatch/FirstTrajectory/20180302213401_route.csv",
                # ),
                (# The second one(*)
                    "./RawData/AiFiMatch/FirstTrajectory/20180302213910_acce.csv",
                    "./RawData/AiFiMatch/FirstTrajectory/20180302213910_gyro.csv",
                    "./RawData/AiFiMatch/FirstTrajectory/20180302213910_wifi.csv",
                    "./RawData/AiFiMatch/FirstTrajectory/20180302213910_route.csv",
                ),
                (# The third one
                    "./RawData/AiFiMatch/FirstTrajectory/20180302214450_acce.csv",
                    "./RawData/AiFiMatch/FirstTrajectory/20180302214450_gyro.csv",
                    "./RawData/AiFiMatch/FirstTrajectory/20180302214450_wifi.csv",
                    "./RawData/AiFiMatch/FirstTrajectory/20180302214450_route.csv",
                ),
            ]
            # initial point and direction
            firstRouteRotClockWise = "0"
            firstMoveVector = (1.2, 1.7)
            rawDataArray.extend(rawDataArrayofFirst)
            routeRotClockWise = firstRouteRotClockWise
            moveVector = firstMoveVector
            dataBelongs = "t1"
        elif trajectorySwitch == 2:
            # TODO: Second trajectory of AiFiMatch
            rawDataArrayofSecond = [
                (# The second one(*)
                    "./RawData/AiFiMatch/SecondTrajectory/20180303165821_acce.csv",
                    "./RawData/AiFiMatch/SecondTrajectory/20180303165821_gyro.csv",
                    "./RawData/AiFiMatch/SecondTrajectory/20180303165821_wifi.csv",
                    "./RawData/AiFiMatch/SecondTrajectory/20180303165821_route.csv",
                ),
                ( # The third one
                    "./RawData/AiFiMatch/SecondTrajectory/20180303170055_acce.csv",
                    "./RawData/AiFiMatch/SecondTrajectory/20180303170055_gyro.csv",
                    "./RawData/AiFiMatch/SecondTrajectory/20180303170055_wifi.csv",
                    "./RawData/AiFiMatch/SecondTrajectory/20180303170055_route.csv",
                )
            ]
            # initial point and direction
            secondRouteRotClockWise = "0"
            secondMoveVector = (49.800, 59.15)
            rawDataArray.extend(rawDataArrayofSecond)
            routeRotClockWise = secondRouteRotClockWise
            moveVector = secondMoveVector
            dataBelongs = "t2"
            pass
        elif trajectorySwitch == 3:
            # TODO: Third Trajectory of AiFiMatch
            rawDataArrayofThird = [
                (# The first one
                    "./RawData/AiFiMatch/ThirdTrajectory/20180303142423_acce.csv",
                    "./RawData/AiFiMatch/ThirdTrajectory/20180303142423_gyro.csv",
                    "./RawData/AiFiMatch/ThirdTrajectory/20180303142423_wifi.csv",
                    "./RawData/AiFiMatch/ThirdTrajectory/20180303142423_route.csv",
                ),
                (  # The fourth one(*)
                    "./RawData/AiFiMatch/ThirdTrajectory/20180303143913_acce.csv",
                    "./RawData/AiFiMatch/ThirdTrajectory/20180303143913_gyro.csv",
                    "./RawData/AiFiMatch/ThirdTrajectory/20180303143913_wifi.csv",
                    "./RawData/AiFiMatch/ThirdTrajectory/20180303143913_route.csv",
                ),
            ]
            # initial point and direction
            thirdRouteRotClockWise = "0"
            thirdMoveVector = (49.8, 1.95)
            rawDataArray.extend(rawDataArrayofThird)
            routeRotClockWise = thirdRouteRotClockWise
            moveVector = thirdMoveVector
            dataBelongs = "t3"

        errorListInSensorError = []
        for i in range(min(len(stepLengthErrorList), len(headingErrorList))):
            slError4Test = stepLengthErrorList[i]
            headingError4Test = headingErrorList[i]
            errorBySteps = []
            for k in range(10):
                for j in range(len(rawDataArray)):
                    filePaths = rawDataArray[j]
                    # Load sensor data from files
                    acceTimeList, acceValueList = loadAcceData(filePaths[0], relativeTime=False)
                    gyroTimeList, gyroValueList = loadGyroData(filePaths[1], relativeTime=False)
                    wifiTimeList, wifiScanList = loadMovingWifi(filePaths[2])
                    # load real locations
                    locRealDF = pd.read_csv(filePaths[3])
                    locRealList = [(loc[0], loc[1]) for loc in locRealDF.values]

                    locEstWorldList = secondAiFi.onlineViterbi(acceTimeList, acceValueList,
                                             gyroTimeList, gyroValueList,
                                             wifiTimeList, wifiScanList,
                                             startingDirection=0.0,
                                             startingPointFlag=True,
                                             startingPoint=moveVector,
                                             stepError=slError4Test,
                                             headingError=headingError4Test
                                             )
                    # Format the estimate locations
                    locEstList = [(round(loc[0] * 1000) / 1000, round(loc[1] * 1000) / 1000) for loc in locEstWorldList]

                    # Calculate the location errors
                    errorList = distError(locRealList, locEstList)
                    errorBySteps.append(errorList)
            errorAvgInTimes = map(lambda errs: np.mean(errs), zip(*errorBySteps))
            print "Step Error ", slError4Test, " Heading Error ", headingError4Test, " Position Error: ", round(np.mean(errorAvgInTimes) * 1000) / 1000
            errorListInSensorError.append((slError4Test, headingError4Test, round(np.mean(errorAvgInTimes) * 1000) / 1000))
        print errorListInSensorError
        if saveFlags[trajectorySwitch-1]:
            errorFilePath = "%s/aifi_error_%s_%s_%s.csv" % (rootDirectory, errorType, dataBelongs, time.strftime("%m%d"))
            errorDF = pd.DataFrame(np.array(errorListInSensorError), columns=["Delta_Step", "Delta_Heading", "Error(m)"])
            errorDF.to_csv(errorFilePath, encoding='utf-8', index=False)
    print("Done.")