#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/1/6 上午12:30
@author: Pete
@email: yuwp_1985@163.com
@file: imagedemo.py
@software: PyCharm Community Edition
"""

import matplotlib.pyplot as plt
import pandas as pd

from PIL import Image,ImageDraw


def showImage(filePath, locationDataFiles):

    im = Image.open(filePath)
    draw = ImageDraw.Draw(im)

    # Load positioning data and draw locations
    colors = ((0, 255, 0), (255, 0, 0), (255, 127, 0), (0, 127, 255))
    for i, locFile in enumerate(locationDataFiles):
        locDF = pd.read_csv(locFile)
        locList = [(loc[0] * (730 / 7.08) + 675, loc[1] * (915 / 10.75) + 150) for loc in locDF.values]
        draw.line(([(loc[1], loc[0]) for loc in locList]), fill=colors[i], width=10)
        for loc in locList:
            bbox = [(loc[1] - 10, loc[0] - 10), (loc[1] + 10, loc[0] + 10)]
            draw.rectangle(bbox, fill=colors[i + 2])

    # Show PNG image
    plt.figure("environment")
    plt.title("PDR Positioning Results")
    plt.axis('off')
    plt.imshow(im)
    plt.show()


if __name__ == "__main__":
    imageFilePath = "./Examples/SimplePDR/20170702210514_environment.png"
    realLocFilePath = "./Examples/SimplePDR/20170702210514_route.txt"
    estiLocFilePath = "./Examples/SimplePDR/20170702210514_estimate.txt"
    showImage(imageFilePath, [realLocFilePath, estiLocFilePath])
    print("Done.")