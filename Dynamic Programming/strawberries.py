profit = [
    [0, 3, 7, 9, 12, 13],
    [0, 5, 10, 11, 11, 11],
    [0, 4, 6, 11, 12, 12]
]


def strawberry(j, s):
    if j == 2:
        return profit[j][s], s
    else:
        return max((profit[j][a] + strawberry(j + 1, s - a)[0], a, s - a) for a in range(0, s + 1))


# we want
print(strawberry(0, 5))
