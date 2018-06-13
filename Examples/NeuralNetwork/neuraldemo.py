#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/6/12 15:20
@author: Pete
@email: yuwp_1985@163.com
@file: neuraldemo.py
@software: PyCharm Community Edition
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import LabelBinarizer
from firstneural import FirstNeuralNetwork

if __name__ == "__main__":
    digits = load_digits()
    X = digits.data
    y = digits.target
    X -= X.min()
    X /= X.max()
    nn = FirstNeuralNetwork([64, 100, 10], activation="logistic")
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    labels_train = LabelBinarizer().fit_transform(y_train)
    labels_test = LabelBinarizer().fit_transform(y_test)
    print "start fitting"
    nn.fit(X_train, labels_train, epochs=30000)
    predictions = []
    for i in range(X_test.shape[0]):
        o = nn.predict(X_test[i])
        predictions.append(np.argmax(o))
    print confusion_matrix(y_test, predictions)
    print classification_report(y_test, predictions)
    print("Done.")