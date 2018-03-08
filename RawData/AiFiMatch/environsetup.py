#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/3/3 18:25
@author: Pete
@email: yuwp_1985@163.com
@file: environsetup.py
@software: PyCharm Community Edition
"""

import matplotlib.pyplot as plt
import pandas as pd

from PIL import Image,ImageDraw

def showImage(filePath, locationDataFiles, routeColors):
    im = Image.open(filePath)
    print(im.size)
    draw = ImageDraw.Draw(im)

    # Load positioning data and draw locations
    firstDF = pd.read_csv(locationDataFiles[0])
    firstLocList = [(loc[0] * (7169 / 56.4) + 30, loc[1] * (10006 / 78.95) + 110) for loc in firstDF.values]
    draw.line(([(loc[1], loc[0]) for loc in firstLocList]), fill=routeColors[0], width=25)

    secondDF = pd.read_csv(locationDataFiles[1])
    secondLocList = [(loc[0] * (7169 / 56.4) + 30, loc[1] * (10006 / 78.95) - 150) for loc in secondDF.values]
    draw.line(([(loc[1], loc[0]) for loc in secondLocList]), fill=routeColors[1], width=25)

    thirdDF = pd.read_csv(locationDataFiles[2])
    thirdLocList = [(loc[0] * (7169 / 56.4) + 30, loc[1] * (10006 / 78.95) + 80) for loc in thirdDF.values]
    draw.line(([(loc[1], loc[0]) for loc in thirdLocList]), fill=routeColors[2], width=25)

    # Show PNG image
    plt.figure("environment")
    plt.title("Ground Truth for Each Trajectory")
    plt.axis('off')
    plt.imshow(im)
    #plt.savefig("./environment_setup.png")
    plt.show()

if __name__ == "__main__":
    imageFilePath = "environment_0302.png"
    firstTrajectoryFilePath = "./FirstTrajectory/20180302213910_route.csv"
    secondTrajectoryFilePath = "./SecondTrajectory/20180303165540_route.csv"
    thirdTrajectoryFilePath = "./ThirdTrajectory/20180303142423_route.csv"
    colors = ((0, 255, 0), (0, 0, 255), (255, 0, 0))
    showImage(imageFilePath, [firstTrajectoryFilePath, secondTrajectoryFilePath, thirdTrajectoryFilePath], colors)
    print("Done.")