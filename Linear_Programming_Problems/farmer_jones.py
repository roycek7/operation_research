#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 12:21:12 2020

@author: royce
"""

"""
Farmer Jones bakes two types of cake (chocolate and plain) to supplement his income. 
Each chocolate cake can be sold for $4 and each plain cake can be sold for $2. 
Each chocolate cake requires 20 minutes of baking time, 250 mL of milk and 4 eggs, 
while each plain cake needs 50 minutes baking, 200 mL of milk and only 1 egg. 
In each day there are eight hours of baking time available. 
Farmer Jones’ hens lay 30 eggs each day and his cows produce 5 L of milk. 
How many of each type of cake should Farmer Jones bake each day to maximize his revenue?
"""

from gurobipy import *

# Define Sets
Cakes = ['Chocolate', 'Plain']
Ingredients = ['Time', 'Eggs', "Milk"]

C = range(len(Cakes))
I = range(len(Ingredients))

# Setup Data
price = [4, 2]
available = [480, 30, 5]

usage = [
    [20, 50],
    [4, 1],
    [0.25, 0.2]
]

##########################################
m = Model("Farmer Jones")

# Add Variables
X = {}
for c in C:
    X[c] = m.addVar()

# Set Objective
m.setObjective(
    quicksum(
        price[c] * X[c] for c in C
    ),
    GRB.MAXIMIZE
)

# Add constraints
m.addConstrs(
    quicksum(
        usage[i][c] * X[c] for c in C) <= available[i] for i in I
)

# Optimize
m.optimize()

# Output result
for c in C:
    print('Bake', X[c].x, Cakes[c])
print("Revenue is", m.objVal)
