#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 12:40:57 2020

@author: royce
"""

"""
George Stigler's 1945 paper “The Cost of Subsistence” (Journal of Farm Economics, 27, 303-314) presents one of the 
earliest applications of linear programming, that of finding minimum-cost diets:
“Elaborate investigations have been made of the adequacy of diets at various income levels, and a considerable number 
of ‘low-cost,’ ‘moderate,’ and ‘expensive’ diets have been recommended to consumers. Yet, so far as I know, 
no one has determined the minimum cost of obtaining the amounts of calories, protein, minerals, and vitamins which
 these studies accept as adequate or optimum.”
 
A Python stub is available on Blackboard which contains some nutritional and cost data for a sample of foods. 
Use this data to determine an optimal diet using these foods.
"""

from gurobipy import *

# Sets
Foods = ['almonds', 'apples', 'apricots', 'banana', 'brie', 'broccoli',
         'brown rice', 'camembert', 'carrots', 'chicken', 'chocolate',
         'couscous', 'cream cheese', 'croissants', 'cucumber', 'currants',
         'custard', 'dark chocolate', 'fried eggs', 'green beans', 'ham',
         'hamburgers', 'hazelnuts', 'herrings', 'mushrooms', 'potato chips',
         'roast pork', 'tomato soup', 'white bread', 'white rice']

Nutrients = ['energy', 'protein', 'fibre', 'iron', 'calcium', 'vitc',
             'thiamin', 'riboflavin', 'vita', 'zinc', 'folate',
             'niacin', 'sodium']

# Costs ($/100g) from coles.com.au [2020-02-26]
C = [1.76, 0.59, 0.89, 0.45, 4.72, 0.69, 0.32, 3.00, 0.22, 0.95, 2.78,
     0.56, 1.88, 1.32, 0.69, 1.63, 0.42, 2.78, 0.56, 1.09, 2.20, 0.90,
     2.67, 1.20, 1.10, 2.06, 1.00, 0.48, 0.49, 0.14]

# Nutritional data from the Australian Food Composition Database
# https://www.foodstandards.gov.au/science/monitoringnutrients/afcd/Pages/default.aspx
NV = [
    [2503, 19.5, 8.8, 3.9, 250, 0, 0.19, 1.4, 2, 3.69, 29, 7.74, 5],
    [206, 0.3, 2.5, 0.17, 3, 5, 0.02, 0.01, 3, 0.07, 0, 0.14, 2],
    [171, 0.8, 2.5, 0.3, 15, 12, 0.025, 0.035, 60, 0.15, 6, 1.38, 2],
    [385, 1.4, 2.4, 0.29, 5, 4, 0.02, 0.047, 6, 0.16, 33, 0.6, 0],
    [1465, 18.6, 0, 0.21, 464, 0, 0.013, 0.483, 371, 2.71, 49, 4.73, 593],
    [129, 4.6, 3.8, 0.85, 33, 57, 0.063, 0.193, 46, 0.6, 31, 1.2, 22],
    [639, 2.9, 1.5, 0.5, 5, 0, 0.14, 0.02, 0, 0.9, 16, 2.35, 3],
    [1286, 19.5, 0, 0.15, 484, 0, 0, 0, 0, 0, 0, 0, 0],
    [132, 0.8, 3.9, 0.28, 30, 6, 0.079, 0.04, 1316, 0.2, 18, 0.9, 40],
    [637, 29, 0, 0.5, 9, 0, 0.05, 0.11, 7, 0.83, 3, 17.7, 46],
    [2206, 7.6, 2.3, 1.42, 252, 5, 0.05, 0.325, 79, 1.24, 36, 1.59, 68],
    [663, 5.2, 2.2, 0.48, 12, 0, 0.064, 0.034, 0, 0.37, 9, 2.41, 6],
    [1384, 8.2, 0, 0.14, 82, 0, 0.05, 0.239, 350, 0.58, 0, 1.65, 336],
    [1500, 10, 2.8, 0.95, 52, 0, 0.11, 0.09, 0, 0.75, 0, 1.67, 457],
    [51, 0.4, 1, 0.27, 57, 13, 0.018, 0.018, 15, 0.18, 0, 0.34, 19],
    [1167, 2.8, 6, 2.3, 87, 0, 0.11, 0, 2, 0.5, 0, 1.47, 46],
    [407, 3.5, 0, 0.05, 120, 0, 0.052, 0.218, 8, 0.41, 0, 0.57, 61],
    [2142, 3.9, 1.2, 4.4, 52, 0, 0.05, 0.13, 21, 2, 13, 1.95, 55],
    [1039, 16.2, 0, 2, 69, 0, 0.1, 0.38, 200, 1.3, 58, 4.74, 146],
    [89, 1.5, 2.5, 1.1, 30, 13, 0.03, 0.07, 77, 0.8, 33, 0.66, 3],
    [467, 17, 1.8, 0.66, 10, 0, 0.386, 0.065, 0, 1.91, 23, 7.17, 1167],
    [974, 12.5, 1.7, 3.1, 74, 1, 0.26, 0.18, 0, 0, 0, 3.89, 477],
    [2689, 14.8, 10.4, 3.2, 86, 0, 0.39, 0.17, 3, 2.2, 113, 4.67, 3],
    [1031, 14.2, 0, 1.2, 77, 0, 0.036, 0.139, 17, 0.5, 2, 5.67, 870],
    [194, 6.2, 2.9, 0.5, 5, 2, 0.042, 0.661, 4, 1.06, 27, 7.02, 15],
    [2160, 6, 3.5, 1.13, 20, 23, 0.16, 0.01, 0, 1.4, 67, 2.68, 618],
    [699, 34.5, 0, 1.35, 6, 0, 0.857, 0.309, 0, 3.67, 2, 10.23, 54],
    [193, 1.4, 0.2, 0.21, 37, 1, 0.127, 0.074, 30, 0.21, 2, 0.87, 360],
    [1027, 9.7, 2.8, 1.48, 62, 0, 0.398, 0.049, 0, 0.83, 254, 6.52, 456],
    [671, 2.7, 1, 0.61, 79, 0, 0.015, 0.02, 0, 0.46, 7, 0.56, 3]
]

# Recommended nutritional requirements for Tindra Lund 
# (a current student at Hofn University on the Islands)
# from Nutrient Reference Values for Australia and New Zealand
# A maximum value of -1 indicates there is no upper limit
DMIN = [8491, 45.4, 23.1, 16.1, 1186, 41.9, 1.1, 1.1, 700, 7.38, 400, 14, 690]
DMAX = [10190, 68.1, -1, 45, 2500, -1, -1, -1, 2875, 36.9, 876.2, -1, 2300]

##################################################################################

m = Model("The Cost of Subsistence")

F = range(len(Foods))
N = range(len(Nutrients))

X = {}
for f in F:
    X[f] = m.addVar()

# Set Objective
m.setObjective(quicksum(C[f] * X[f] for f in F), GRB.MINIMIZE)

# Set constraints
for i in N:
    m.addConstr(quicksum(NV[f][i] * X[f] for f in F) >= DMIN[i])
    if DMAX[i] > 0:
        m.addConstr(quicksum(NV[f][i] * X[f] for f in F) <= DMAX[i])

# Optimize
m.optimize()

# Output
for f in F:
    if X[f].x > 0:
        print(Foods[f], round(100 * X[f].x))
print('Cost is', m.objVal)
