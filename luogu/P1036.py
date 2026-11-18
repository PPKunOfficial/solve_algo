import sys
from functools import cache


@cache
def is_prime(v: int) -> bool:
    if v < 2:
        return False
    if v % 2 == 0:
        return v == 2
    if v % 3 == 0:
        return v == 3

    i = 5
    while i * i <= v:
        if v % i == 0 or v % (i + 2) == 0:
            return False
        i += 6
    return True


def main():
    n, k = map(int, sys.stdin.buffer.readline().split())
    x = list(map(int, sys.stdin.buffer.readline().split()))

    ans = 0

    def dfs(start, cnt, tot):
        nonlocal ans
        need = k - cnt
        if cnt == k:
            if is_prime(tot):
                ans += 1
            return
        end = n - need + 1
        for i in range(start, end):
            dfs(i + 1, cnt + 1, tot + x[i])

    dfs(0, 0, 0)
    print(ans)


main()
