"""
Tutorial 7 – Coal Line Maintenance
Throughput of coal from mine to port to ship is a critical issue for Australia’s largest coal systems. Press reports of
huge queues of ships waiting to be loaded are common and these queues are expensive for the industry. A typical but
simple diagram for a coal system is shown below.

Coal is moved by train from the coal mines along the lines until it meets the shared unloading facility, where there
are two unloaders. From the unloaders it is moved via conveyer belt into the stockpile, using stackers. From the
stackers it is removed using reclaimers, and again moved by conveyer belt through the loaders on to ships. There is an
option to bypass the stockpile completely.
Part A
More generally, we can describe a coal system using a collection of nodes and arcs. Some of the nodes are source nodes
(mines) and some are sink nodes (ships). For each arc we know the origin and destination nodes and the maximum weekly
throughput of the arc.
a) Develop a linear programming model of a general coal system that determines how much coal to move on each arc so as
to maximise the total throughput. This throughput is the total amount of coal moved out of the source nodes, which will
be equal to the total amount of coal moved into the sink nodes. For all other nodes the total amount of coal moved into
the node will be same as the total amount of coal moved out of the node. For the purposes of this model you can ignore
the time lag of coal moving through the system with respect to the weekly schedule.
b) In order to keep the system running smoothly, it needs to be maintained. Assume we are given a set of maintenance
tasks applying to the arcs, with at most one task for each arc. For each arc we know whether or not it has a maintenance
 task and the effort (in man days) for the maintenance task.
We wish to schedule all the known maintenance tasks over the next T weeks. For each week we know the maximum man days
available for maintenance, which may vary from week to week.
Assume that each maintenance task must be started and finished in the same week, and that when an arc is being
maintained its throughput goes down to 0 for the whole week.
Develop a mixed integer programming model to produce a maintenance schedule for the next T weeks so as to maximise the
total throughput.

The effort estimates are given in person-days. Each week they can carry out a maximum of 110 person-days of maintenance.
 Each maintenance activity must be carried out completely within a week. What is the optimal maintenance schedule that
 will give the maximum throughput in those four weeks?
Part C
They would also like to examine the impact if they could add some additional requirements that would assist the
maintenance teams. Specifically, the following would help:
1) Carrying out maintenance on Stockpile Bypass in the first week
2) Carrying out maintenance on Stacker 3 before Stacker 4
3) Finishing maintenance on Stacker 2 at least one week before maintenance on Stacker 1 is started
How would these constraints affect the maximum throughput?
"""
from gurobipy import *

# Sets
Nodes = [0, 3, 4, 5, 6, 7, 8]
T = range(4)
# SSNodes = [0, 1, 2, 8, 9]

Arcs = {
    'Line1': (0, 4),
    'Line2': (0, 3),
    'Line3': (0, 3),
    'Line4': (3, 4),
    'Unload1': (4, 5),
    'Unload2': (4, 5),
    'Bypass': (5, 7),
    'Stacker1': (5, 6),
    'Stacker2': (5, 6),
    'Stacker3': (5, 6),
    'Stacker4': (5, 6),
    'Reclaim1': (6, 7),
    'Reclaim2': (6, 7),
    'Reclaim3': (6, 7),
    'Load1': (7, 8),
    'Load2': (7, 8),
    'Back': (8, 0)
}

# Data
throughput = {
    'Line1': 100,
    'Line2': 60,
    'Line3': 60,
    'Line4': 100,
    'Unload1': 80,
    'Unload2': 80,
    'Bypass': 20,
    'Stacker1': 40,
    'Stacker2': 40,
    'Stacker3': 40,
    'Stacker4': 40,
    'Reclaim1': 50,
    'Reclaim2': 50,
    'Reclaim3': 50,
    'Load1': 75,
    'Load2': 75
}

maintain = {
    'Line3': 50,
    'Unload2': 15,
    'Bypass': 55,
    'Stacker1': 30,
    'Stacker2': 20,
    'Stacker3': 70,
    'Stacker4': 20,
    'Reclaim1': 35,
    'Reclaim2': 35,
    'Load1': 45
}

days = [110 for t in T]

m = Model("Coal Line Maintenance")

X = {}
Y = {}
for a in Arcs:
    for t in T:
        X[a, t] = m.addVar()
        Y[a, t] = m.addVar(vtype=GRB.BINARY)

m.setObjective(quicksum(X['Back', t] for t in T), GRB.MAXIMIZE)

for a in throughput:
    for t in T:
        m.addConstr(X[a, t] <= throughput[a] * (1 - Y[a, t]))

for n in Nodes:
    for t in T:
        # if n not in SSNodes:
        m.addConstr(quicksum(X[a, t] for a in Arcs if Arcs[a][1] == n) ==
                    quicksum(X[a, t] for a in Arcs if Arcs[a][0] == n))

# m.addConstr(X['Load1'] + X['Load2'] == X['Line1'] + X['Line2'] + X['Line3'])

for t in T:
    m.addConstr(quicksum(Y[a, t] * maintain[a] for a in maintain) <= days[t])

for a in maintain:
    m.addConstr(quicksum(Y[a, t] for t in T) == 1)

m.addConstr(Y['Bypass', 0] == 1)

# Y['Stacker4', 0] <= 0
# Y['Stacker4', 1] <= Y['Stacker3', 0]
# Y['Stacker4', 2] <= Y['Stacker3', 1] + Y['Stacker3', 0]
for t in T:
    m.addConstr(Y['Stacker4', t] <= quicksum(Y['Stacker3', u] for u in T if u < t))

# Y['Stacker1', 0] <=0
# Y['Stacker1', 1] <=0
# Y['Stacker1', 2] <= Y['Stacker2', 0]
# Y['Stacker1', 3] <= Y['Stacker2', 1] + Y['Stacker2', 0]
for t in T:
    m.addConstr(Y['Stacker1', t] <= quicksum(Y['Stacker2', u] for u in T if u + 1 < t))

m.optimize()

print('Throughput')
for a in Arcs:
    print(a, [X[a, t].x for t in T])

print('\nMaintanance')
for a in maintain:
    for t in T:
        if Y[a, t].x > 0.9:
            print('Maintain', a, 'in week', t + 1)
    # print(a, [round(Y[a, t].x) for t in T])
