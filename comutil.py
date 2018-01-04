#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/1/4 9:15
@author: Pete
@email: yuwp_1985@163.com
@file: comutil.py
@software: PyCharm Community Edition
"""

import numpy as np
import scipy.signal as signal


def butterFilter(data, fs=50, lowcut=0.5, highcut=4.0, order=2):
    """
    Apply butterworth filter to the raw data
    :param data: raw data
    :param fs: sample frequency
    :param lowcut: low frequency threshold
    :param highcut: high frequency threshold
    :param order: butterworth band pass in  order value, 2 by default
    :return: filtered data
    """
    # butter band pass
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    dataArray = np.array(data).astype(np.float)
    y = signal.lfilter(b, a, dataArray)
    return y


if __name__ == "__main__":
    print("Done.")