import sys
from bisect import bisect_left


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    a = [next(it) for _ in range(n)]

    m = next(it)
    q = [next(it) for _ in range(m)]

    pre_b = [0] * (n + 1)
    for i in range(1, n + 1):
        pre_b[i] = pre_b[i - 1] + a[i - 1]

    ans = []
    for x in q:
        ans.append(str(bisect_left(pre_b, x)))

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    main()
