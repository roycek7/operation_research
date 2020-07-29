# Data
rainfall = [2, 1, 1]  # per season
unit_revenue = [50, 100, 150]  # per season
capacity = 3  # dam capacity in water height (m)
# Stages (i): growing seasons
# State (s): dam capacity (height in m) at start of season t
# Actions (a): water release to make from dam in season (in m)
# Value function: V(t,s) = maximise revenue from future crops given we are at
#                          stage i with state s (dam capacity) at start of i
#                          overall cost function
_V = {}


def C(i, use):
    return unit_revenue[i] * (use + rainfall[i] - 0.1 * (use + rainfall[i]) ** 2)


def V(i, s):
    if i is 3:
        return 0, 0
    else:
        if (i, s) not in _V:
            _V[i, s] = max((C(i, use) + V(i + 1, min(capacity, s + rainfall[i] - use))[0], use, s + rainfall[i] - use)
                           for use in range(0, min(capacity, s) + 1))
        return _V[i, s]


print(V(0, 3))
print(V(1, 3))
print(V(2, 2))
