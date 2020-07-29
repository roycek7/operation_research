#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 12:21:12 2020

@author: royce
"""
from gurobipy import *

# Part 1

# This is an example of using a dictionary to define a set and associated data
Products = {
    'Cars (Germany)': 10.3,
    'Cars (Japan)': 10.1,
    'Computers (USA)': 11.8,
    'Computers (Singapore)': 11.4,
    'Appliances (Europe)': 12.7,
    'Appliances (Asia)': 12.2,
    'Insurance (Germany)': 9.5,
    'Insurance (USA)': 9.9,
    'Short-term bonds': 3.6,
    'Medium-term bonds': 4.2
}

m = Model("Portfolio Optimisation")

# X[p] is amount to invest in product p (in first year)
X = {p: m.addVar() for p in Products}

m.setObjective(quicksum(Products[p] * X[p] / 100 for p in Products), GRB.MAXIMIZE)

# Create a dictionary of the constraints so we can access them later for
# sensitivity analysis
Constraints = {
    'Total': m.addConstr(quicksum(X[p] for p in Products) <= 100000),
    'Cars': m.addConstr(X['Cars (Germany)'] + X['Cars (Japan)'] <= 30000),
    'Computers': m.addConstr(X['Computers (USA)'] + X['Computers (Singapore)'] <= 30000),
    'Appliances': m.addConstr(X['Appliances (Europe)'] + X['Appliances (Asia)'] <= 20000),
    'Insurance': m.addConstr(X['Insurance (Germany)'] + X['Insurance (USA)'] >= 20000),
    'Bonds': m.addConstr(X['Short-term bonds'] + X['Medium-term bonds'] >= 25000),
    'Balance': m.addConstr(X['Short-term bonds'] >= 0.4 * X['Medium-term bonds']),
    'Germany': m.addConstr(X['Cars (Germany)'] + X['Insurance (Germany)'] <= 50000),
    'USA': m.addConstr(X['Computers (USA)'] + X['Insurance (USA)'] <= 40000)
}

m.optimize()
for p in Products:
    print(p, X[p].x)
print("Total return = $", m.objVal)

# Sensitivity Analysis (to answer (b) and (c) in Part 1)
# See the lecture notes from Week 3 for details
print("Sensitivity Analysis - Constraints")
# PI is dual variable
for c in Constraints:
    print(c, Constraints[c].RHS, Constraints[c].Slack, round(Constraints[c].PI, 3),
          Constraints[c].SARHSLow, Constraints[c].SARHSUp)
print("Dual objective = $", sum(Constraints[c].RHS * Constraints[c].Pi for c in Constraints))

print("Sensitivity Analysis - Variables")
# RC is reduced cost
for p in Products:
    print(p, round(X[p].obj, 3), X[p].x, round(X[p].RC, 3), round(X[p].SAObjLow, 3), round(X[p].SAObjUp, 3))

# Part 2

# Business as usual, downturn, upturn, crash
ScenarioProb = [0.8, 0.15, 0.04, 0.01]
S = range(len(ScenarioProb))

Year2Return = {
    'Cars (Germany)': [10.3, 5.1, 11.8, -30.0],
    'Cars (Japan)': [10.1, 4.4, 12.0, -35.0],
    'Computers (USA)': [11.8, 10.0, 12.5, 1.0],
    'Computers (Singapore)': [11.4, 11.0, 11.8, 2.0],
    'Appliances (Europe)': [12.7, 8.2, 13.4, -10.0],
    'Appliances (Asia)': [12.2, 8.0, 13.0, -12.0],
    'Insurance (Germany)': [9.5, 2.0, 14.7, -5.4],
    'Insurance (USA)': [9.9, 3.0, 12.9, -4.6],
    'Short-term bonds': [3.6, 4.2, 3.1, 5.9],
    'Medium-term bonds': [4.2, 4.7, 3.5, 6.3]
}

# X[p] is unchanged
# Y[p,s] is the amount to invest in product p under scenario s in Year 2
Y = {(p, s): m.addVar() for p in Products for s in S}

# As with variables, we can also add a dictionary of constraints for s in S
Year2Total = {s: m.addConstr(quicksum(Y[p, s] for p in Products) <= 100000) for s in S}

# Constrain amounts to be within $10,000 of year 1
Year2LinkUp = {(p, s): m.addConstr(Y[p, s] <= X[p] + 10000) for (p, s) in Y}
Year2LinkDown = {(p, s): m.addConstr(Y[p, s] >= X[p] - 10000) for (p, s) in Y}

m.setObjective(quicksum(Products[p] * X[p] / 100 for p in Products) +
               quicksum(ScenarioProb[s] * Year2Return[p][s] * Y[p, s] / 100 for (p, s) in Y),
               GRB.MAXIMIZE)

# Note that we can optimise a model again within the same file, now with
# the additional Y variables, constraints and updated objective
m.optimize()
for p in Products:
    print(p, X[p].x)

for s in S:
    print('************', ScenarioProb[s])
    for p in Products:
        print(p, Y[p, s].x)



