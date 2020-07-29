revHigh = 800
revLow = 600


def advertise(t, s):
    if t == 5:
        return 0, 'done'
    else:
        if s == 'high':
            yes = 0.8 * (revHigh - 70 + advertise(t + 1, 'high')[0]) + \
                  0.2 * (revLow - 70 - 80 + advertise(t + 1, 'low')[0])
            no = 0.6 * (revHigh + advertise(t + 1, 'high')[0]) + 0.4 * (revLow - 80 + advertise(t + 1, 'low')[0])
        else:
            yes = 0.6 * (revHigh - 70 - 80 + advertise(t + 1, 'high')[0]) + \
                  0.4 * (revLow - 70 + advertise(t + 1, 'low')[0])
            no = 0.2 * (revHigh - 80 + advertise(t + 1, 'high')[0]) + 0.8 * (revLow + advertise(t + 1, 'low')[0])
        return max((yes, 'yes'), (no, 'no'))


print(advertise(4, 'high'))
print(advertise(1, 'low'))
print(advertise(2, 'high'))
print(advertise(2, 'low'))
print(advertise(3, 'high'))
print(advertise(3, 'low'))
print(advertise(4, 'high'))
print(advertise(4, 'low'))