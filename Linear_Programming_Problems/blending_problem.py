"""
Created on Thu Mar 5 08:40:57 2020

@author: royce
"""

"""
A food manufacturer refines raw oils and blends them together. The raw oils come in two categories – vegetable oils, 
of which there are two types; and non- vegetable oils, of which there are three types.
The oils are refined on different production lines. In any month it is not possible to refine more than 200 tonnes of 
vegetable oil and more than 250 tonnes of non-vegetable oils. There is no loss of mass in the refining process and 
the cost of refining may be ignored.
There is a technological restriction on the “hardness” of the final product. In the units in which hardness is 
measured it must lie between 3 and 6. The hardness of a blended product is the weighted average of its components.
The cost per tonne and hardness of the raw oils are:
   
   Oil  | Cost | Hardness
   Veg 1  $110    8.8 
   Veg 2  $120    6.1 
   Oil 1  $130    2.0 
   Oil 2  $110    4.2 
   Oil 3  $115    5.0
   
The final product sells for $150 per tonne.
How should the food manufacturer make this product in order to maximise net profit?
"""

from gurobipy import *

# Define Sets
oils = ['Veg 1', 'Veg 1', 'Oil 1', 'Oil 2', 'Oil 3']
O = range(len(oils))

# Define Data
cost = [110, 120, 130, 110, 115]
selling_price = 150
hardness = [8.8, 6.1, 2.0, 4.2, 5.0]
is_veg = [True, True, False, False, False]
max_veg_amount = 200
max_non_veg_amount = 250
min_hardness = 3
max_hardness = 6

##########################################
m = Model("Blending Problem")

# Add Variables
X = {}
for i in O:
    X[i] = m.addVar()

# Set Objective
m.setObjective(
    quicksum(
        (selling_price - cost[i]) * X[i] for i in O
    )
    , GRB.MAXIMIZE)

# Add constraints
m.addConstr(
    quicksum(
        X[i] for i in O if is_veg[i]) <= max_veg_amount
)

m.addConstr(
    quicksum(
        X[i] for i in O if not is_veg[i]) <= max_non_veg_amount
)

m.addConstr(
    quicksum(
        (hardness[i] - min_hardness) * X[i] for i in O) >= 0
)

m.addConstr(
    quicksum(
        (hardness[i] - max_hardness) * X[i] for i in O) <= 0
)

# Optimize
m.optimize()

# Output
for i in O:
    print(f"{oils[i]} processes {round(X[i].x, 2)} tonnes")

print(f"net profit: {m.objVal}")

# hardness
# print('Checking Hardness', sum([hardness[i]*X[i].x for i in O])/sum([X[i].x for i in O]))
