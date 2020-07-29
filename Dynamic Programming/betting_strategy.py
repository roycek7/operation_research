p = 0.4


def bets(j, s):
    if j == 3:
        if s >= 5:
            return 1, 'yay'
        else:
            return 0, 'sigh'
    else:
        return max((p * bets(j + 1, s + b)[0] + (1 - p) * bets(j + 1, s - b)[0], b) for b in range(0, s + 1))


print(bets(0, 2))

# want bets(0, 2) = (0.256, 2)
# so bet $2 in first game
# if you win bet $1 in second game
# if you get the third game (with $4), bet $2 or $3
