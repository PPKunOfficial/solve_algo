import sys
from functools import cache

sys.setrecursionlimit(10000)

n = int(sys.stdin.readline())


# i表示可入栈的数 j表示可出栈的数
@cache
def f(i, j):
    if i == 0:
        return 1
    res = f(i - 1, j + 1)  # push
    if j > 0:
        res += f(i, j - 1)  # pop
    return res


print(f(n, 0))
