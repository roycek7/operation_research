"""
Knapsack Problem
We have a container of size 20 units, and want to pack it with the following valuable items:
Item j Size vj Value tj
1 7 25
2 4 12
3 3 8
How many of each item should we pack in order to maximize the total value?
"""
import sys

sys.setrecursionlimit(1500000)

sizes = [7, 4, 3]
values = [25, 12, 8]
J = range(len(sizes))

# Knap(s) is max value from packing a knapsack of size s
_Knap = {}


def Knap(s):
    if s < 3:
        return 0, -1
    else:
        if s not in _Knap:
            _Knap[s] = max((values[a] + Knap(s - sizes[a])[0], 'Item {}'.format(a + 1),
                            s - sizes[a]) for a in J if sizes[a] <= s)
        return _Knap[s]


print(Knap(20))
