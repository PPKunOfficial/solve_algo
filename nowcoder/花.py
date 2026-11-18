import sys
from functools import cache


@cache
def f(x, y, z):
    if z == 1:
        return x
    if z == 2:
        return y
    if z >= 3:
        return (f(x, y, z - 1) + f(x, y, z - 2)) % 998244353

    return 0


def main():
    t = int(sys.stdin.buffer.readline())
    for _ in range(t):
        n = int(sys.stdin.buffer.readline())
        a = list(map(int, sys.stdin.buffer.readline().split()))
        tot = 0
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                tot += f(a[i - 1], a[j - 1], j - i + 1)
        print(tot)


main()
