#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2017/12/27 14:51
@author: Pete
@email: yuwp_1985@163.com
@file: CdfDemo.py
@software: PyCharm Community Edition
"""

import numpy as np
import matplotlib.pyplot as plt

"""
The empirical CDF is usually defined as
CDF(x) = "number of samples <= x" / "number of samples"
"""

if __name__ == "__main__":
    # Create some test data
    dx = 0.1
    X = np.arange(-2, 2 + dx, dx)
    Y = np.exp(-X**2)

    # Normalize the data to a proper PDF
    Y /= (dx * Y).sum()
    # Compute the CDF
    CY = np.cumsum(dx * Y)

    # Plot the function
    plt.plot(X, Y)
    plt.plot(X, CY, "r--")
    plt.show()

    print("Done.")