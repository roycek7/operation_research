P = range(4)
C = range(10)


# Stages: Draws
# State: Card we have just drawn; Current board
# Actions: Choosing one of the empty positions to place the card
# Value function: cards() returns the minimum expected value if we get "card"
#                 when we have board in state "board"
_V = {}


def cards(card, board):
    # here we use -1 to indicate an empty spot
    # so board is full when everything is >= 0
    if min(board) >= 0:
        return (10 * board[0] + board[1]) * (10 * board[2] + board[3]), 'Done'
    else:
        best = 10000, 0
        for a in P:
            if board[a] < 0:
                # make a new board with the card inserted at position a
                new = [board[k] for k in P]
                new[a] = card
                # next stage we could get any of the available cards, b,
                # with equal probability prob
                available = [c for c in C if c not in board and c is not card]
                prob = 1 / len(available)
                # print(f'card: {card}, board: {board}, new: {new}, available: {available}, prob: {prob}')
                s = sum(prob * cards(b, new)[0] for b in available)
                if s < best[0]:
                    best = s, a
        return best


# what should we do if a particular first card is dealt?
def firstcard(card):
    return cards(card, [-1, -1, -1, -1])


for t in range(10):
    print(firstcard(t))
