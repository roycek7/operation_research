def stamps_required(stamps, postage):
    s = [0] + [postage + 1] * postage
    s[0] = 0
    for stamp in range(postage + 1):
        for denomination in stamps:
            if denomination <= stamp:
                s[stamp] = min(s[stamp], 1 + s[stamp - denomination])
    if s[postage] > postage:
        return
    else:
        return s[postage]


print(stamps_required([1, 7, 12], 14))
