"""
Bird Song
______________
A male bird needs to sing in order to find a mate but also needs to spend time foraging to survive.
How should he split his time between these two tasks?
We will split a time horizon of one day into 150 time segments (just under 10 minutes each) where the bird is able to
decide his behaviour in each segment. Time 0 is dawn, time 75 is dusk and time 150 is dawn of the following day.
During each day segment (0– 74) he can sing, forage or rest. During each night segment (75–149) he can only rest.
We will denote the bird’s food reserves by i. If the reserves reach 0 then the bird dies of starvation.
Singing
If the bird has reserves i and spends a time segment singing then he will use 𝐷 food reserves where
𝐷 = 12 + 0.002𝑖 + 𝐵
where 𝐵 is -6.4, 0, 6.4 with probabilities 0.25, 0.50, 0.25, respectively.
In each time segment that the bird is singing he has a probability of 0.004 of pairing with a mate.
Foraging
If the bird instead spends a time segment foraging then he will use 𝐷 food reserves where
𝐷 = 8 + 0.007𝑖 + 𝐵
where 𝐵 is as for singing.
In each time segment that the bird is foraging he has a probability of 0.6
of finding a food patch that gives him 𝐸 = 32 food reserves.
Resting
If the bird spends a time segment resting then he uses 𝐷 = 3.6 food
reserves.
At the end of each time segment let 𝑥 = 𝑖 + 𝐸 − 𝐷 and 𝑝 = 𝑥 − ⌊𝑥⌋. Then the food reserves at the start of the next
time segment will be ⌊𝑥⌋ + 1 with probability 𝑝 and ⌊𝑥⌋ with probability 1 − 𝑝.
At the end of the whole time horizon (time 150) the bird receives 2 points if he has a mate, 1 point if he is alive but
has not found a mate, and 0 points if he is dead. What is the optimal strategy that the male bird should pursue?
"""
import pylab


psing = 0.004
pforage = 0.6
restfood = 3.6
foodpatch = 32


def singfood(i):
    return 12 + 0.002 * i


def foragefood(i):
    return 8 + 0.007 * i


def SongDash(t, x, m):
    i = int(x)
    p = x - i
    return p * Song(t, i + 1, m)[0] + (1 - p) * Song(t, i, m)[0]


def SongBlur(t, i, m):
    return 0.25 * SongDash(t, i - 6.4, m) + 0.5 * SongDash(t, i, m) + 0.25 * SongDash(t, i + 6.4, m)


_Song = {}


def Song(t, i, m):
    if i <= 0:
        return 0, 'dead'
    elif t == 150:
        if m == 1:
            return 2, 'mate'
        else:
            return 1, 'lonely'
    else:
        if (t, i, m) not in _Song:
            if t >= 75:
                _Song[t, i, m] = (SongDash(t + 1, i - restfood, m), 'rest')
            else:
                rest = SongDash(t + 1, i - restfood, m)
                sing = psing * SongBlur(t + 1, i - singfood(i), 1) + \
                       (1 - psing) * SongBlur(t + 1, i - singfood(i), m)
                forage = pforage * SongBlur(t + 1, i - foragefood(i) + foodpatch, m) + \
                         (1 - pforage) * SongBlur(t + 1, i - foragefood(i), m)
                _Song[t, i, m] = max((rest, 'rest'), (sing, 'sing'), (forage, 'forage'))
        return _Song[t, i, m]


def SingThreshold(t):
    i = 1
    while Song(t, i, 0)[1] != 'sing':
        i += 1
    return i


thresholds = [SingThreshold(t) for t in range(75)]
pylab.plot(range(75), thresholds)
pylab.xlabel('Time Period')
pylab.ylabel('Food Reserve required to sing')
pylab.show()

print(Song(150, -5, 1))
print(Song(150, 10, 1))
print(Song(150, 10, 0))
print(Song(149, 10, 0))
print(Song(149, 10, 1))
print(Song(149, 3, 1))
print(Song(75, 100, 1))
print(Song(75, 400, 1))
print(Song(74, 400, 1))
print(Song(70, 300, 1))
print(Song(70, 2700, 1))
print(Song(70, 270, 1))
print(Song(0, 40, 0))
print(Song(0, 200, 0))
print(SingThreshold(50))
