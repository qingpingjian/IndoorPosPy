#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/6/11 14:56
@author: Pete
@email: yuwp_1985@163.com
@file: firstneural.py
@software: PyCharm Community Edition
"""
import numpy as np

def tanh(x):
    return np.tanh(x)

def tanh_deriv(x):
    return 1.0 - np.tanh(x) * np.tanh(x)

def logistic(x):
    return 1.0 / (1.0 + np.exp(-x))

def logistic_deriv(x):
    return logistic(x) * (1.0 - logistic(x))

class FirstNeuralNetwork(object):
    def __init__(self, layers, activation="tanh"):
        """
        :param layers: A list containing the number of units in each layers
        :param activation: The activation function to be used, it can be
        'logistic' or 'tanh'
        """
        if activation == "logistic":
            self.activation = logistic
            self.activation_deriv = logistic_deriv
        elif activation == "tanh":
            self.activation = tanh
            self.activation_deriv = tanh_deriv
        self.weights = []
        # TODO: 这里的weights似乎是多了一些，用来存放偏向(bias)
        for i in range(1, len(layers)):
            if i == len(layers) - 1:
                self.weights.append((2 * np.random.random((layers[i - 1] + 1, layers[i])) - 1) * 0.25)
            else:
                self.weights.append((2 * np.random.random((layers[i-1] + 1, layers[i] + 1)) - 1) * 0.25)
        return

    def fit(self, X, y, learning_rate=0.2, epochs=10000):
        X = np.atleast_2d(X) # 一行对应一个实例, 一列对应一个特征
        temp = np.ones([X.shape[0], X.shape[1]+1])
        temp[:, 0:-1] = X # adding the bias unit to the input layer，不懂，感觉就是为X增加了一列1
        X = temp
        y = np.array(y)

        for k in range(epochs):
            i = np.random.randint(X.shape[0])
            a = [X[i]] # 只有一行的二维数组,随机取到一个实例，最后一个单元是1.0初始时

            # 这部分代码假设偏置都为0
            for l in range(len(self.weights)):
                a.append(self.activation(np.dot(a[l], self.weights[l])))
            error = y[i] - a[-1] # Computer the error at the top layer
            deltas = [error * self.activation_deriv(a[-1])] # 更新之后的误差

            # starting back propagation,最后输出层的公式不一样，输入层不需要
            for l in range(len(a) -2, 0, -1):
                deltas.append(deltas[-1].dot(self.weights[l].T)*self.activation_deriv(a[l]))
            deltas.reverse()
            # 权重更新 w_ij learing_rate * i层的输出 * j层的误差
            for i in range(len(self.weights)):
                layer = np.atleast_2d(a[i])
                delta = np.atleast_2d(deltas[i])
                self.weights[i] += learning_rate * layer.T.dot(delta)

    def predict(self, x):
        x = np.array(x)
        temp = np.ones(x.shape[0]+1)
        temp[0:-1] = x
        a = temp
        for l in range(0, len(self.weights)):
            a = self.activation(np.dot(a, self.weights[l]))
        return a



if __name__ == "__main__":
    # XOR运算（非线性） 神经网络模拟
    nn = FirstNeuralNetwork([2,2,1])
    X = np.array([[0,0], [0, 1], [1, 0], [1,1]])
    y = np.array([0, 1, 1, 0])
    nn.fit(X, y, epochs=10000)
    for i in [[0,0], [0, 1], [1, 0], [1,1]]:
        print i,
        print " XOR operation by Neural Network predicting result: ", nn.predict(np.array(i))
    print("Done.")