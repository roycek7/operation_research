from gurobipy import *

S = range(16)
P = range(4)

Squares = [
    [(4, 8, 12, 13), (9, 10, 11, 13), (2, 3, 7, 11), (7, 9, 10, 11), (10, 12, 13, 14)],
    [(2, 6, 9, 10), (4, 8, 9, 10), (0, 1, 4, 8), (2, 3, 6, 10), (0, 1, 2, 6), (8, 9, 10, 14)],
    [(0, 1, 4, 5), (1, 2, 5, 6), (5, 6, 9, 10), (4, 5, 8, 9)],
    [(3, 7, 11, 15), (12, 13, 14, 15)]]

I = [range(len(Squares[p])) for p in P]

m = Model('Heist Puzzle')

X = {}
for p in P:
    for i in I[p]:
        X[p, i] = m.addVar(vtype=GRB.BINARY)

for s in S:
    m.addConstr(
        quicksum(X[p, i] for p in P for i in I[p] if s in Squares[p][i]) == 1
    )

for p in P:
    m.addConstr(
        quicksum(X[p, i] for i in I[p]) == 1
    )


while True:
    m.optimize()
    if m.status == GRB.INFEASIBLE:
        break

    for p in P:
        for i in I[p]:
            if X[p, i].x > 0.9:
                print(Squares[p][i])
    m.addConstr(
        quicksum(X[p, i] for (p, i) in X if X[p, i].x > 0.9) <= 3
    )