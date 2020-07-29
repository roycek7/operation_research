_V = {}


# Stages: game, rounds
# State: probability, probability of co-operating
# Action:
# V(t,p) gives maximum expected value from starting game t with probability p of cooperating
def V(game, probability):
    if game is 10:
        return 0, 0
    else:
        if (game, probability) not in _V:
            cooperate = probability * (3 + V(game + 1, min(1, probability + 0.1))[0]) + \
                        (1 - probability) * (0 + V(game + 1, min(1, probability + 0.1))[0])
            defect = probability * (5 + V(game + 1, max(0, probability - 0.2))[0]) + \
                     (1 - probability) * (1 + V(game + 1, max(0, probability - 0.2))[0])
            _V[game, probability] = max((cooperate, 'Co-operate'), (defect, 'Defect'))
    return _V[game, probability]


print('---------------------------')
prob = 0.6
# Transitions are deterministic so we can generate sequence of actions
for games in range(10):
    payoff, decision = V(games, prob)
    print('|Round', games + 1, '\t|\t', decision)
    prob = min(1, prob + 0.1) if decision == 'Co-operate' else max(0, prob - 0.2)
