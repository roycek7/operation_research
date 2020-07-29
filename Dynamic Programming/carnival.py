# Data

Points = [6, 4, 10, 7]

ProbMiss = [0.8, 0.6, 0.9, 0.5]

Shots = 10

# Stages: i, shots on target

# States: S, probability of a target not being hit

# Action: a, target to aim for

# ValueFunction V(i, S): Maximum expected points given the previous shots thrown.

_V = {}


def V(i, S):
    if i == Shots:
        return 0, "All shots used"
    if (i, tuple(S)) not in _V:
        choices = []
        for a in range(len(Points)):
            c = S[a] * (1 - ProbMiss[a]) * Points[a]
            p = S[a] * ProbMiss[a]
            S = S[:a] + (p,) + S[a + 1:]
            choices.append((c + V(i + 1, S)[0], a))
        _V[(i, tuple(S))] = max(choices)
    return _V[(i, tuple(S))]


S = (1, 1, 1, 1)
print(f"Expected Score: {V(0, S)[0]}")

for i in range(Shots):
    points, a = V(i, S)
    print(f"Shot {i + 1} aim for {a + 1}, Total points: {points}")
    p = S[a] * ProbMiss[a]
    S = S[:a] + (p,) + S[a + 1:]
