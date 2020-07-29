import sys

sys.setrecursionlimit(1500000)

_Fib = {}


def Fib(n):
    if n not in _Fib:
        if n <= 2:
            _Fib[n] = 1
        else:
            _Fib[n] = Fib(n - 1) + Fib(n - 2)
    return _Fib[n]


print(Fib(0))
