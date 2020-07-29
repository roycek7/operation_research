edges = {
    ('A', 'B'): 10,
    ('A', 'C'): 7,
    ('A', 'D'): 6,
    ('B', 'E'): 9,
    ('C', 'E'): 7,
    ('D', 'E'): 11,
    ('D', 'F'): 7,
    ('E', 'G'): 8,
    ('E', 'H'): 7,
    ('E', 'I'): 10,
    ('F', 'G'): 8,
    ('F', 'G'): 6,
    ('F', 'I'): 7,
    ('G', 'J'): 13,
    ('H', 'J'): 8,
    ('I', 'J'): 9
}


def joe(i):
    if i == 'J':
        return 0, 'Done'
    else:
        return min((max(edges[road], joe(road[1])[0]), road[1]) for road in edges if road[0] == i)


print(joe('A'))
