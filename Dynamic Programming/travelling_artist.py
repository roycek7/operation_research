costs = [
    [0, 143, 108, 118, 121, 88, 121, 57, 92],     # Home
    [143, 0, 35, 63, 108, 228, 182, 73, 162],     # A
    [108, 35, 0, 45, 86, 193, 165, 42, 129],      # B
    [118, 63, 45, 0, 46, 190, 203, 73, 105],      # C
    [121, 108, 86, 46, 0, 172, 224, 98, 71],      # D
    [88, 228, 193, 190, 172, 0, 174, 160, 108],   # E
    [121, 182, 165, 203, 224, 174, 0, 129, 212],  # F
    [57, 73, 42, 73, 98, 160, 129, 0, 117],       # G
    [92, 162, 129, 105, 71, 108, 212, 117, 0]     # H
]

sales = [
    [0.0, 0.0, 0.0],  # Home
    [0.3, 0.4, 0.3],  # A
    [0.2, 0.5, 0.3],  # B
    [0.2, 0.7, 0.1],  # C
    [0.3, 0.5, 0.2],  # D
    [0.3, 0.6, 0.1],  # E
    [0.4, 0.3, 0.3],  # F
    [0.0, 0.3, 0.7],  # G
    [0.1, 0.1, 0.8]   # H
]

Cities = range(len(costs))

Home = 0

# Part A - can precalculate the expected sales

ESales = [sum(k * sales[i][k] for k in [0, 1, 2]) for i in Cities]


# V(S,i) is max expected profit if we are currently at city i having visited cities S
def V(S, i):
    if len(S) == 4:
        return -costs[i][Home], Home
    return max((500 * ESales[j] - costs[i][j] + V(S + [j], j)[0], j) for j in Cities if j not in S)


# V([],Home) = 2364 following Home -> 8 -> 2 -> 1 -> 7 -> Home

# Part B

_V2 = {}


def V2(S, i, p):
    if (len(S) == 4) or (p == 0):
        return -costs[i][Home], Home
    if (tuple(S), i, p) not in _V2:
        _V2[tuple(S), i, p] = max((-costs[i][j] +
                                   sum(sales[j][k] * (500 * min(k, p) + V2(S + [j], j, p - min(k, p))[0]) for k in
                                       [0, 1, 2]), j)
                                  for j in Cities if j not in S)
    return _V2[tuple(S), i, p]


# V2([],Home,5) = $2033.63
# Home -> G -> B
# If 4 paintings after B -> A -> H

# If 1,2,3 paintings after B -> C -> H

# After H -> Home


# print(V([8, 2, 1, 7], 7))
print(V2([], Home, 5))
