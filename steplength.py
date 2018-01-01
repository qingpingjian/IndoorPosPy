#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2017/12/21 下午10:42
@author: Pete
@email: yuwp_1985@163.com
@file: steplength.py
@software: PyCharm Community Edition
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from scipy.optimize import leastsq

# Environment Configuration
matplotlib.rcParams['font.size'] = 15
# matplotlib.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签
# matplotlib.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

"""
Step Length Model: s = h(af + b) + c
where:
h is height of body
f is step frequency
a, b, c is parameters of this model

Experimental Raw Data of Pete:
stepLength,stepFrequency
72.53, 1.67
77.08, 1.78
75.97, 1.77
79.53, 1.91
66.42, 1.70
66.53, 1.74
76.96, 1.94
74.07, 1.88
70.89, 1.65
72.99, 1.78
76.94, 1.89
76.27, 1.92
"""


# Step Length Model
def fitFunc(para, x):
    k, b = para
    return k * x + b


# residuals function
def residualsFunc(para, y, x):
    ret = fitFunc(para, x) - y
    return ret

if __name__ == "__main__":
    # Pete
    stepLengthList = [72.53, 77.08, 75.97, 79.53, 66.42, 66.53, 76.96, 74.07, 70.89, 72.99, 76.94, 76.27]
    stepFrequencyList = [1.67, 1.78, 1.77, 1.91, 1.70, 1.74, 1.94, 1.88, 1.65, 1.78, 1.89, 1.92]

    # Super Ma
    stepLengthList = [86.65, 86.4, 80.95, 82.4, 82.3, 88.9, 88.6, 92.25, 88.4, 88.45,
                      88.55, 88.45, 89.75, 89.9, 90.05, 82.4, 78.05, 82.6, 82.45, 81.65,
                      79.1, 76.7, 77.95, 79.55, 80.2]
    stepFrequencyList = [1.61, 1.82, 1.62, 1.69, 1.73, 1.94, 1.99, 2.07, 1.98, 1.96,
                         1.86, 1.84, 1.87, 1.89, 2.10, 1.65, 1.52, 1.72, 1.63, 1.58,
                         1.49, 1.52, 1.65, 1.61, 1.44]

    # Format raw experimental data
    stepLengthArray = np.array(stepLengthList)
    stepLengthArray = stepLengthArray.astype(np.float)
    stepFrequencyArray = np.array(stepFrequencyList)
    stepFrequencyArray = stepFrequencyArray.astype(np.float)

    # Random initial parameter
    pInit = np.random.randn(2)
    # Least square algorithm
    pLSQ = leastsq(residualsFunc, pInit, args=(stepLengthArray, stepFrequencyArray))
    paraK, paraB = pLSQ[0]
    if paraB < 0:
        print("The fit function is Ls = %f * Fs %f" % (paraK, paraB))
    else:
        print("The fit function is Ls = %f * Fs + %f" % (paraK, paraB))
    # Mean step length
    print("The mean step length is %.2f" % (paraK * float(np.mean(stepFrequencyArray)) + paraB))

    # The fit function is Ls = 28.927316 * Fs + 21.706846 - Pete
    # The mean step length is 73.85
    # The fit function is Ls = 21.853894 * Fs + 46.235461 - Super Ma
    # The mean step length is 84.51

    # Plot the fit function
    plt.xlabel("$Step Frequency(Hz)$")
    plt.ylabel("$Step Length(cm)$")
    plt.scatter(stepFrequencyArray, stepLengthArray, color="red", linewidths=2)
    plt.plot(stepFrequencyArray, stepFrequencyArray * paraK + paraB, color="blue", linewidth=2)
    plt.show()
    print("Done.")