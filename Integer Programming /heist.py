from gurobipy import *

# List of pieces which are stored within a bounding rectangle
# Each piece has two entries, one for each side
# Coded as:
#   - is a blank square
#   . is a lock
#   X is a missing square
#   | is the end of the piece
#     other letters are colours White, Blue, Red, Green

PData = [
    ["-.-|.-X", "W-.|X.-"],
    [".XX|-.-|XX.", "XX-|.-.|-XX"],
    ["-.-|.XX|-XX", "-.-|XXW|XX-"],
    ["-X-|.-.", "-X-|.-R"],
    ["X.X|.-X|X.-", "X-X|X.-|.-X"],
    ["X.|.-|X.|X-", "-X|.-|-X|.X"],
    ["X.|.-|X.", ".X|-.|RX"],
    ["B-X|X.-|XX.", "X-.|-.X|.XX"],
    ["X-X|-.-|X-X", "X.X|.-.|X.X"],
    [".-.-.", ".-.-G"],
    ["X-|-.|.X|-X", ".X|-.|X-|X."],
    ["X.|X-|X.|.-", "-X|.X|-X|.-"],
    ["XX-|.-B|XX-", "-XX|.-.|-XX"]
]

# Challenge 1 is RBW in corner
BData1 = [
    ".-.-.-.-",
    "-.-.-.-.",
    ".-.-.-.-",
    "-.-.-.-.",
    ".-.-.-.-",
    "-.-.-.-R",
    ".-.-.-B-",
    "-.-.-W-."]

BData2 = [
    ".-.-.-.-",
    "-R-.-.-.",
    ".-.-.-.-",
    "-.-.-.-.",
    ".-.-.-.-",
    "-.-.-.-.",
    ".-.-.-W-",
    "-.-.-.-."]

BData3 = [
    ".-.-.-.-",
    "-.-.-.-.",
    ".-.-.-.-",
    "-.-.-.-.",
    ".-.-.-.-",
    "-.-.-.-.",
    ".-.-.-W-",
    "-.-.-.-."]

BData4 = [
    ".-.-.-.-",
    "-.-.-.-.",
    ".-.-.-.-",
    "-.-.-.-.",
    ".-.-.-.-",
    "-.-.-.-.",
    ".-.-.-.-",
    "-.-.-.-."]

BData = BData2

# Pull the PData apart
# P will contain a list of pairs of lists of matrices of letters
P = []
for pd in PData:
    P.append([[], []])
    if len(pd[0]) != len(pd[1]):
        print("Mismatch 1", pd[0], pd[1])
    p0 = pd[0].split("|")
    p1 = pd[1].split("|")
    if len(p0) != len(p1):
        print("Mismatch 2", pd[0], pd[1])
    ll = len(p0[0])
    for pp in p0:
        if len(pp) != ll:
            print("Mismatch 3", pd[0], pd[1])
        P[-1][0].append(list(pp))
        for c in pp:
            if c not in "X.-WBRG":
                print("Mismatch 3a", pd[0], pd[1])
    for pp in p1:
        if len(pp) != ll:
            print("Mismatch 4", pd[0], pd[1])
        P[-1][1].append(list(pp))
        for c in pp:
            if c not in "X.-WBRG":
                print("Mismatch 4a", pd[0], pd[1])
    for pp0, pp1 in zip(P[-1][0], P[-1][1]):
        for i in range(ll):
            if pp0[i] == 'X':
                if pp1[ll - i - 1] != 'X':
                    print("Mismatch 5a", pd[0], pd[1])
            else:
                if pp1[ll - i - 1] == 'X':
                    print("Mismatch 5b", pd[0], pd[1])

## Setup B
B = [list(bd) for bd in BData]
NB = len(B)
N = range(NB)

PR = range(len(P))

## We want to generate a list of placements for each piece
## Each placement is a sorted tuple of 3-tuples.  The 3-tuples contain
## the offset co-ordinates and the type of dot
RList = [[] for p in PR]
# For each piece
for p in PR:
    # for each flip
    for f in [0, 1]:
        rows = len(P[p][f])
        cols = len(P[p][f][0])
        R = [(i, j, P[p][f][i][j]) for i in range(rows)
             for j in range(cols) if P[p][f][i][j] != 'X']
        tr = tuple(sorted(R))
        if tr not in RList[p]:
            RList[p].append(tr)
        for rot in range(3):
            # Rotate the piece 90 degrees
            R = [(j, rows - i - 1, c) for (i, j, c) in tr]
            rows, cols = cols, rows
            tr = tuple(sorted(R))
            if tr not in RList[p]:
                RList[p].append(tr)


def CanPlace(tlist, i, j):
    for t in tlist:
        if i + t[0] >= NB or j + t[1] >= NB or B[i + t[0]][j + t[1]] != t[2]:
            return False
    return True


mod = Model('Heist')
X = {(p, r, i, j): mod.addVar(vtype=GRB.BINARY)
     for p in PR for r in range(len(RList[p])) for i in N for j in N
     if CanPlace(RList[p][r], i, j)}

LIJ = [[[] for j in N] for i in N]
LP = [[] for p in PR]
for (p, r, i, j) in X:
    LP[p].append(X[p, r, i, j])
    for t in RList[p][r]:
        LIJ[i + t[0]][j + t[1]].append(X[p, r, i, j])

[mod.addConstr(quicksum(LP[p]) == 1, name="P{0}".format(p)) for p in PR]
[mod.addConstr(quicksum(LIJ[i][j]) == 1, name="IJ{0},{1}".format(i, j)) for i in N for j in N]

while True:
    mod.optimize()
    if mod.Status == GRB.INFEASIBLE:
        break

    Board = [[' ' for j in N] for i in N]
    PS = []
    for (p, r, i, j) in X:
        if X[p, r, i, j].x > 0.9:
            PS.append(X[p, r, i, j])
            for t in RList[p][r]:
                Board[i + t[0]][j + t[1]] = "ABCDEFGHIJKLM"[p]

    for i in N:
        print("".join(Board[i]))
    # Remove this next break to generate all possible solutions
    break
    mod.addConstr(quicksum(PS) <= len(PS) - 1)

