#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2017/12/27 14:51
@author: Pete
@email: yuwp_1985@163.com
@file: CdfDemo.py
@software: PyCharm Community Edition
"""

import math
import matplotlib.pyplot as plt
import numpy as np
import sys


"""
The empirical CDF is usually defined as
CDF(x) = "number of samples <= x" / "number of samples"
"""
def cdf(data, hasDuplicate=True):
    sortedData = np.sort(data)
    dataLength = len(sortedData)
    cdfData = np.arange(1, dataLength + 1) / float(dataLength)
    retValue = (sortedData, cdfData)
    if hasDuplicate:
        distinctData = [sortedData[-1]]
        distinctCDF = [1.0]
        for i in range(dataLength - 2, -1, -1):
            if math.fabs(distinctData[-1] - sortedData[i]) > sys.float_info.epsilon:
                distinctData.append(sortedData[i])
                distinctCDF.append(cdfData[i])
        retValue = (np.array(distinctData), np.array(distinctCDF))
    return retValue


if __name__ == "__main__":
    # some test data
    data = [0.02, 0.02, 0.1, 0.1, 0.2, 0.2, 0.3, 0.3, 0.4, 0.4, 0.6, 0.8, 1., 1.2, 1.2, 1.4]
    # Calculate the CDF
    X, Y = cdf(data)
    X2, Y2 = cdf(data, False)

    # Plot the function
    plt.grid(True)
    plt.plot(X2, Y2, marker="o")
    plt.plot(X, Y, "r--", marker="*")
    plt.show()

    print("Done.")