#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017/11/9 9:54
@author: Pete
@email: yuwp_1985@163.com
@file: jwdcluser.py
@software: PyCharm Community Edition
'''

import time as tm
import jwdtools as jdt
import pandas as pd

def findDistWeight(dist, distCluster):
    counter = 0
    for d in distCluster:
        if d < dist:
            break
        counter = counter + 1
    return counter / len(distCluster)

def loadUserData(shopInfoFilePath, userBehaFilePath, testFilePath):
    shopInfoData = pd.read_csv(shopInfoFilePath)
    shopJwd = shopInfoData.iloc[:, [0,2,3]]
    shopDict = {}
    for shop in shopJwd.values:
        shopDict[shop[0]] = (shop[1], shop[2])
    userBehaData = pd.read_csv(userBehaFilePath)
    userJwd = userBehaData.iloc[:, [0, 1, 3, 4]]
    jwdDict = {}
    for user in userJwd.values:
        shop_id = user[1]
        longShop, latiShop = shopDict[shop_id]
        if jwdDict.has_key(shop_id):
            jwdDict[shop_id].append(jdt.distance(longShop, latiShop, user[2], user[3]))
        else:
            jwdDict[shop_id] = [jdt.distance(longShop, latiShop, user[2], user[3])]
    for shop_id in jwdDict.keys():
        jwdDict[shop_id] = sorted(jwdDict[shop_id], reverse=True)
    testData = pd.read_csv(testFilePath)
    testJwd = testData.iloc[:, [0, 4, 5]]
    predictResults = []
    for testRecord in testJwd.values:
        rowID = testRecord[0]
        testLong = testRecord[1]
        testLati = testRecord[2]
        distStat = []
        for shop_id in jwdDict.keys():
            longShop, latiShop = shopDict[shop_id]
            distStat.append((shop_id, findDistWeight(jdt.distance(testLong, testLati, longShop, latiShop), jwdDict[shop_id])))
        shopPredict = sorted(distStat, key=lambda x:x[1], reverse=True)[0][0]
        predictResults.append("%s,%s\n" % (rowID, shopPredict))
    return predictResults



if __name__ == "__main__":
    shopInfoFilePath = "./训练数据-ccf_first_round_shop_info.csv".decode(encoding='utf-8')
    userBehaFilePath = "./训练数据-ccf_first_round_user_shop_behavior.csv".decode(encoding='utf-8')
    testFilePath = "./AB榜测试集-evaluation_public.csv".decode(encoding="utf-8")
    results = loadUserData(shopInfoFilePath, userBehaFilePath, testFilePath)
    resultFilePath = ("./result_%s.csv" % int(tm.time())).decode(encoding='utf-8')
    headLine = "row_id,shop_id\n"
    with open(resultFilePath, 'wb') as resultFile:
        resultFile.write(headLine)
        resultFile.writelines(results)
    print("Done.")
