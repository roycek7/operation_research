# Data
Req = [155, 120, 140, 100, 155]
MaxReq = max(Req)


# Stage: Seasons (t)
# State: Operators at the start of season (s)
# Action: Hire (+) or fire (-) operators (a)
# Value function: total cost from season t to end, starting with s operators

# Note that feasibility is handled through the range() calculation

def V(t, s):
    if t == 4:
        return 200 * (Req[4] - s) ** 2, Req[4] - s
    else:
        return min((200 * a ** 2 + 2000 * (s + a - Req[t]) + V(t + 1, s + a)[0], a)
                   for a in range(Req[t] - s, MaxReq - s + 1))


s = 155
for t in range(5):
    total, a = V(t, s)
    s += a
    print('Total', total, "Season", t + 1, "Hire", a, "Operators", s)
