"""
Chess Strategy
Vladimir is playing Keith in a two-game chess match. Winning a game scores one match point and drawing a game scores
a half match point. After the two games are played, the player with more match points is declared the champion.
If the two players are tied after two games, they continue playing until somebody wins a game (the winner of that game
will be the champion).
During each game, Vladimir can play one of two ways: boldly or conservatively. If he plays boldly, he has a 45% chance
of winning the game and a 55% chance of losing the game. If he plays conservatively, he has a 90% chance of drawing
the game and a 10% chance of losing the game.
What strategy should Vladimir follow to maximize his probability of winning the match?
"""


# Chess(t, s) is the max probability of winning match if we start game t with s points
# we want Chess(1, 0)
def Chess(t, s):
    if t == 3:
        if s < 1:
            return 0, 'Lost'
        elif s > 1:
            return 1, 'Won'
        else:
            return 0.45, 'Bold'
    else:
        bold = 0.45 * Chess(t + 1, s + 1)[0] + 0.55 * Chess(t + 1, s + 0)[0]
        conservative = 0.9 * Chess(t + 1, s + 1 / 2)[0] + 0.10 * Chess(t + 1, s + 0)[0]
        return max((bold, 'Bold'), (conservative, 'Conservative'))


print(Chess(1, 0))
