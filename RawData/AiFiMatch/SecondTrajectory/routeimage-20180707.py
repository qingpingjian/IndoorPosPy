#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/3/3 上午1:00
@author: Pete
@email: yuwp_1985@163.com
@file: routeimage.py
@software: PyCharm Community Edition
"""

import matplotlib.pyplot as plt
import pandas as pd

from PIL import Image,ImageDraw

def showImage(filePath, locationDataFiles, routeColors):
    im = Image.open(filePath)
    print(im.size)
    draw = ImageDraw.Draw(im)

    # secondDF = pd.read_csv(locationDataFiles[1])
    # secondLocList = [(loc[0] * (7169 / 56.4) + 30, loc[1] * (10006 / 78.95) - 150) for loc in secondDF.values]
    # draw.line(([(loc[1], loc[0]) for loc in secondLocList]), fill=routeColors[1], width=25)
    # Load positioning data and draw locations
    #colors = ((0, 255, 0), (255, 0, 0), (255, 127, 0), (0, 127, 255))
    for i, locFile in enumerate(locationDataFiles):
        locDF = pd.read_csv(locFile)
        #locList = [(loc[0] * (7169 / 56.4) + 30, loc[1] * (10006 / 78.95) - 150) for loc in locDF.values]
        locList = [(loc[0] * (5777 / 62.4) + 175, loc[1] * (8101 / 78.95) - 196) for loc in locDF.values]
        draw.line(([(loc[1], loc[0]) for loc in locList]), fill=routeColors[i], width=25)
        # for loc in locList:
        #     bbox = [(loc[1] - 10, loc[0] - 10), (loc[1] + 10, loc[0] + 10)]
        #     draw.rectangle(bbox, fill=colors[i + 2])

    # Show PNG image
    plt.figure("environment")
    #plt.title("Offline Positioning Results")
    plt.axis('off')
    plt.imshow(im)
    plt.show()

if __name__ == "__main__":
    imageFilePath = "../20180705-envrionment-aifi.png"
    estiLocFilePath = "20180303165821_estimate_pdr.csv"
    #estiLocFilePath = "20180303165540_estimate_pdr.csv"
    offlineFilePath = "20180303165821_estimate_aifi_offline.csv"
    colors = ((0, 0, 255), (255, 0, 0))
    showImage(imageFilePath, [estiLocFilePath, offlineFilePath], colors)
    print("Done.")