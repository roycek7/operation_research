# Data
sales = [14, 8, 17, 22, 12, 6]

# Stages: Weeks, t
# State: books on hand at the start of week, s
# Action: boxes to purchase
# Value Function: V(t, s) = maximum total profit of sales given we are in week t with s
#                           books in storage at start of week.

_V = {}


def V(t, s):
    if t is 6:
        return 1 * s - 0.5 * s, 0
    else:
        if (t, s) not in _V:
            best = -100, 0
            for a in range(9):
                sold = min(sales[t], s + 10 * a)
                profit = 12 * sold - 0.5 * s - 50 * a + V(t + 1, s + 10 * a - sold)[0]
                if profit > best[0]:
                    best = profit, f'{a} boxes to purchase i.e {10 * a} books', \
                           f'{s + 10 * a - sold} books left on shelf'
            _V[t, s] = best
        return _V[t, s]


def V1(t, s):
    if t is 6:
        return 1 * s - 0.5 * s, 0
    else:
        if (t, s) not in _V:
            _V[t, s] = max(
                (12 * min(sales[t], s + 10 * a) - 0.5 * s - 50 * a +
                 V1(t + 1, s + 10 * a - min(sales[t], s + 10 * a))[0],
                 f'{a} boxes to purchase i.e {10 * a} books',
                 f'{s + 10 * a - min(sales[t], s + 10 * a)} books left on shelf')
                for a in range(9)
            )
        return _V[t, s]


print(V1(0, 0))
print(V1(1, 6))
print(V1(2, 8))
print(V1(3, 1))
print(V1(4, 9))
print(V1(5, 7))

########################################################################################################################
# Stages: Weeks, t
# State: books on hand at the start of week, s; has movie been announced?, m
# Action: boxes to purchase
# Value Function: V2(t, s) = maximum total profit of sales given we are in week t with s
#                           books in storage at start of week and
#                           movie has been announced (m + 1) or not announced(m = 0)


_V2 = {}


def V2(t, s, m):
    if t is 6:
        return 1 * s - 0.5 * s, 0
    else:
        if (t, s, m) not in _V2:
            best = -100, 0
            for a in range(9):
                # if movie not announced
                sold_0 = min(sales[t], s + 10 * a)
                profit = 12 * sold_0 - 0.5 * s - 50 * a + V2(t + 1, s + 10 * a - sold_0, 0)[0]
                # if movie has been announced
                sold_1 = min(2 * sales[t], s + 10 * a)
                profit1 = 12 * sold_1 - 0.5 * s - 50 * a + V2(t + 1, s + 10 * a - sold_1, 1)[0]

                if m is 1:
                    profit = profit1
                else:
                    profit = 0.3 * profit1 + 0.7 * profit

                if profit > best[0]:
                    best = profit, a
            _V2[t, s, m] = best
        return _V2[t, s, m]


print(V2(0, 0, 0))
