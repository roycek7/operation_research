#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 12:49:59 2020

@author: royce
"""

from gurobipy import *

# Set up your data
profit = [10, 6, 8, 4, 11, 9, 3]
P = range(len(profit))

n = [4, 2, 3, 1, 1]
M = range(len(n))

# usage[P][M]
usage = [
    [0.5, 0.1, 0.2, 0.05, 0.00],
    [0.7, 0.2, 0.0, 0.03, 0.00],
    [0.0, 0.0, 0.8, 0.00, 0.01],
    [0.0, 0.3, 0.0, 0.07, 0.00],
    [0.3, 0.0, 0.0, 0.10, 0.05],
    [0.2, 0.6, 0.0, 0.00, 0.00],
    [0.5, 0.0, 0.6, 0.08, 0.05]
]

T = range(6)

# maintenance[T][M]
maint = [
    [1, 0, 0, 0, 0],
    [0, 0, 2, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 1, 0, 1]
]

# market[P][T]
market = [
    [500, 600, 300, 200, 0, 500],
    [1000, 500, 600, 300, 100, 500],
    [300, 200, 0, 400, 500, 100],
    [300, 0, 0, 500, 100, 300],
    [800, 400, 500, 200, 1000, 1100],
    [200, 300, 400, 0, 300, 500],
    [100, 150, 100, 100, 0, 60]
]

maxstore = 100
storecost = 0.5
endstore = 50
initialstore = 0
monthhours = 16 * 24

fp = Model('Factory Planning')

# variables
X = {}
S = {}
Y = {}
Z = {}
for p in P:
    for t in T:
        X[p, t] = fp.addVar(vtype=GRB.INTEGER)
        S[p, t] = fp.addVar(vtype=GRB.INTEGER)
        Y[p, t] = fp.addVar(vtype=GRB.INTEGER)
        for m in M:
            Z[t, m] = fp.addVar(vtype=GRB.INTEGER)

fp.setObjective(quicksum(profit[p] * Y[p, t]
                         for p in P for t in T) -
                quicksum(storecost * S[p, t]
                         for p in P for t in T),
                GRB.MAXIMIZE)
for p in P:
    fp.addConstr(
        S[p, 0] == X[p, 0] - Y[p, 0] + initialstore
    )

    fp.addConstr(
        S[p, 5] == endstore
    )

    for t in T:
        fp.addConstr(
            S[p, t] <= maxstore
        )
        fp.addConstr(
            Y[p, t] <= market[p][t]
        )
        if t > 0:
            fp.addConstr(
                S[p, t] == X[p, t] - Y[p, t] + S[p, t - 1]
            )

for m in M:
    fp.addConstr(
        quicksum(
            Z[t, m] for t in T) == sum(maint[t][m] for t in T
                                       )
    )

for t in T:
    fp.addConstr(
        quicksum(
            Z[t, m] for m in M) <= 3
    )

for m in M:
    for t in T:
        fp.addConstr(
            quicksum(
                usage[p][m] * X[p, t] for p in P) <= monthhours * (n[m] - Z[t, m]
                                                                   )
        )

fp.optimize()

print('Profit = $', fp.objVal)
print('Sales')
for p in P:
    print(p, [int(Y[p, t].x) for t in T])

print('Production')
for p in P:
    print(p, [int(X[p, t].x) for t in T])

print('Storage')
for p in P:
    print(p, [int(S[p, t].x) for t in T])

print('Maintain')
for m in M:
    print(p, [int(Z[t, m].x) for t in T])
