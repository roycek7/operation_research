#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 8 17:41:27 2020

@author: royce
"""

from gurobipy import *

Grid = [
    [0, 0, 0,   4, 3, 1,   0, 0, 0],
    [0, 0, 8,   0, 0, 0,   4, 0, 0],
    [0, 3, 0,   0, 0, 0,   0, 1, 0],

    [2, 0, 0,   0, 0, 0,   0, 0, 5],
    [3, 0, 0,   0, 6, 0,   0, 0, 9],
    [9, 0, 0,   0, 0, 0,   0, 0, 2],

    [0, 7, 0,   0, 0, 0,   0, 6, 0],
    [0, 0, 9,   0, 0, 0,   5, 0, 0],
    [0, 0, 0,   8, 5, 3,   0, 0, 0],
]

N = range(9)
K = range(1, 10)

m = Model()

X = {}
for i in N:
    for j in N:
        for k in K:
            X[i, j, k] = m.addVar(vtype=GRB.BINARY)

for i in N:
    for j in N:
        if Grid[i][j] > 0:
            # PreAssign
            m.addConstr(
                X[i, j, Grid[i][j]] == 1
            )

        # One per Square
        m.addConstr(
            quicksum(
                X[i, j, k] for k in K) == 1
        )

    for k in K:
        # Each value in Row
        m.addConstr(
            quicksum(
                X[i, j, k] for j in N) == 1
        )

for j in N:
    for k in K:
        # Each value in Column
        m.addConstr(
            quicksum(
                X[i, j, k] for i in N) == 1
        )

for ii in range(3):
    for jj in range(3):
        for k in K:
            m.addConstr(
                quicksum(
                    X[i, j, k] for i in range(3 * ii, 3 * ii + 3)
                    for j in range(3 * jj, 3 * jj + 3)) == 1
            )

m.optimize()

print('----+-----+----')
for i in N:
    if i == 3 or i == 6:
        print('----+-----+----')
    for j in N:
        if j == 3 or j == 6:
            print(' | ', end='')
        for k in K:
            if X[i, j, k].x > 0.9:
                print(k, sep='', end='')
    print('')
print('----+-----+----')
