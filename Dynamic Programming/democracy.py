reps = [1.2, 1.4, 0.4]


def cities(j, s):
    if j == 2:
        return abs(reps[j] - s), s
    else:
        return min((max(abs(reps[j] - a), cities(j + 1, s - a)[0]), a, s - a) for a in range(0, s + 1))


print(cities(0, 3))

# want cities(0, 3)
