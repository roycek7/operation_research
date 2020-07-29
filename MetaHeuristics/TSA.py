import math
import random
import pylab


def Distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


nLoc = 150
N = range(nLoc)
Square = 1000
random.seed(nLoc)
Pos = [(random.randint(0, Square), random.randint(0, Square)) for i in N]
D = [[Distance(Pos[i], Pos[j]) for j in N] for i in N]


def Cost(Path):
    return sum(D[Path[i - 1]][Path[i]] for i in N)


Path = list(N)
random.shuffle(Path)


def ChooseNeigh(Path):
    while True:
        i = random.choice(N)
        j = random.choice(N)
        if j < i:
            i, j = j, i
        if i != j and j - i < nLoc - 1:
            break
    a1 = Path[i - 1]
    a2 = Path[i]
    b1 = Path[j]
    b2 = Path[(j + 1) % nLoc]
    return D[a1][b1] + D[a2][b2] - (D[a1][a2] + D[b1][b2]), (i, j)


def MoveToNeigh(Path, neigh):
    i, j = neigh
    for k in range(int((j - i + 1) / 2)):
        Path[i + k], Path[j - k] = Path[j - k], Path[i + k]


def RunSA(Solution, Cost, ChooseNeigh, MoveToNeigh, N, T, alpha):
    E = Cost(Solution)
    Best = E
    CostArr = [E]
    BestArr = [Best]
    for i in range(N):
        delta, neighbour = ChooseNeigh(Solution)
        if delta < 0 or random.random() < math.exp(-delta / T):
            MoveToNeigh(Solution, neighbour)
            E += delta
            if E < Best:
                Best = E
        CostArr.append(E)
        BestArr.append(Best)
        T *= alpha
    print(E)
    pylab.plot(range(N + 1), CostArr)
    pylab.plot(range(N + 1), BestArr)
    pylab.show()


RunSA(Path, Cost, ChooseNeigh, MoveToNeigh, 1000000, Square, 0.999994)

print(Cost(Path))

pylab.plot([Pos[Path[i]][0] for i in range(-1, nLoc)], [Pos[Path[i]][1] for i in range(-1, nLoc)])
pylab.show()
