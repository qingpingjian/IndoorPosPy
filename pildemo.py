# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw
import matplotlib.pyplot as plt
from dataloader import  loadRouteData
import pandas as  pd
im = Image.open('./RawData/SimplePDR/20170702210514_environment.png') # 读取图片
draw = ImageDraw.Draw (im)
print(im.size)

locationFilePath = "./RawData/SimplePDR/20170702210514_route.txt"
locRealList = loadRouteData(locationFilePath)
locationList = [(loc[0]*(730/7.08)+675, loc[1]*(915/10.75)+150) for loc in locRealList]
print(locationList)
draw.line(([(loc[1], loc[0]) for loc in locationList]), fill = (0,255,0), width = 10)
for loc in locationList:
    bbox = [(loc[1], loc[0]), (loc[1]-20, loc[0]-20)]
    draw.rectangle(bbox, fill=(255,0,0), outline=(255,0,0))

locationFilePath2 = "./RawData/SimplePDR/20170702210514_estimate.txt"
locRealList = loadRouteData(locationFilePath2)
locationList2 = [(loc[0]*(730/7.08)+675, loc[1]*(915/10.75)+150) for loc in locRealList]
print(locationList2)
draw.line(([(loc[1], loc[0]) for loc in locationList2]), fill = (255,0,0), width = 10)
for loc in locationList2:
    bbox = [(loc[1], loc[0]), (loc[1]-20, loc[0]-20)]
    draw.rectangle(bbox, fill=(0,0,255), outline=(0,0,255))

plt.figure("environment")
plt.imshow(im)
plt.show()