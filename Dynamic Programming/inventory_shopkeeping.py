demands = [1, 2, 3, 3, 2, 2]

M = range(len(demands))


# minimum cost of meeting demand if we start month t with 10s units in stock
def V(t, s):
    if t is 5:
        if s >= demands[t]:
            return 1 * s + 0, 0
        else:
            a = demands[t] - s
            return 1 * s + 20 + 20 * a, a
    else:
        best = 1000, 0
        for a in range(max(0, demands[t] - s), 7):
            c = 1 * s  # storage cost
            if a > 0:
                c = c + 20 + 20 * a
            c = c + V(t + 1, s + a - demands[t])[0]
            if c < best[0]:
                best = c, a
        return best


print("-----------------------------------------")
print("Month", '\t\t|\t', "order", '\t\t|\t', 'cost')
print("-----------------------------------------")
s = 0
for t in M:
    cost, a = V(t, s)
    print("Month", t + 1, '\t|\t', "order", a, '\t|\t', 'cost', cost)
    s += a - demands[t]
print("-----------------------------------------")
