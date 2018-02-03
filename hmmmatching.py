#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/2/3 21:53
@author: Pete
@email: yuwp_1985@163.com
@file: hmmmatching.py
@software: PyCharm Community Edition
"""
import numpy as np

baseDirect = 1.25   # direction in radian
# floorplan abstraction including straight parts of corridor and rooms
# for corridor (id, length, direction)
# for room (id, width(door), length, door-right-corner, door-left-corner)
abstractMap = [(1, 7.9, 0.0),
               (2, 40.6, 1.57),
               (3, 17.9, 0.0),
               (4, 8.9, 5.49, 5.35, 4.71),
               (5, 8.9, 5.49, 1.57, 0.78)]

class SimpleHMM(object):
    def __init__(self, Ann, Bnm, pi) :
        self.A = np.array(Ann)      # transition matrix
        self.B = np.array(Bnm)      # emission matrix
        self.pi = np.array(pi)      # initial vector
        self.N = self.A.shape[0]    # N hidden state
        self.M = self.B.shape[1]    # M observable state

#==============================================================================
#   Finding the probability of an observed sequence
#   for a given observed sequence, we calculate the forward probabilities
#   with all existing HMMs, then we can find the most probal model.
#==============================================================================
    def forward(self, O) :
        T = len(O)
        # alpha[t, i] : At time t, the probability of state is i
        alpha = np.zeros((T, self.N))
        # Initialization
        for i in range(self.N):
            alpha[0, i] = self.pi[i] * self.B[i, O[0]]

        # Induction
        for t in range(T-1) :
            for j in range(self.N) :
                sum = 0.0
                for i in range(self.N) :
                    sum += alpha[t,i] * self.A[i,j]
                alpha[t+1, j] = sum * self.B[j, O[t+1]]

        # Summarize
        prob = 0.0
        for j in range(self.N) :
            prob += alpha[T-1, j]
        return prob

#==============================================================================
#   given an observed sequence and HMM model, find the most probable
#   hidden state sequence and its probability.
#   delta[t, i] : at time t, the most probal state sequence to i, also means
#   partial optimal path.
#   hiddenSequence: the final hidden state sequence
#==============================================================================
    def viterbi(self, O) :
        T = len(O)
        delta = np.zeros((T, self.N), np.float)
        bkPointers = np.zeros((T, self.N), np.float)
        hiddenSequence = np.zeros(T, np.int)

        # Initialize
        for i in range(self.N) :
            delta[0, i] = self.pi[i] * self.B[i, O[0]]
            bkPointers[0, i] = 0

        # Induction
        for t in range(1, T) :
            for i in range(self.N) :
                delta[t, i] = self.B[i, O[t]] * np.array([delta[t-1, j] * self.A[j, i] for j in range(self.N)]).max()
                bkPointers[t, i] = np.array([delta[t-1, j] * self.A[j, i] for j in range(self.N)]).argmax()

        # Summarize
        prob = delta[T-1].max()
        hiddenSequence[T-1] = delta[T-1].argmax()
        # Get the hidden state sequence
        for t in range(T-2, -1, -1) :
            hiddenSequence[t] = bkPointers[t+1, hiddenSequence[t+1]]
        return hiddenSequence, prob

    def baumwelch(self, O, alpha, beta, gamma) :
        print "Baum_Welch Algorithm"


    def printHMM(self) :
        print "========================================"
        print "HMM content: N = ", self.N, " M = ", self.M
        print "HMM.pi ", self.pi
        for i in range(self.N) :
            if i == 0 :
                print "HMM.A  ", self.A[i]
            else :
                print "       ", self.A[i]
        for i in range(self.N) :
            if i == 0 :
                print "HMM.B  ", self.B[i]
            else :
                print "       ", self.B[i]
        print "========================================"

if __name__ == "__main__":
    print("Done.")