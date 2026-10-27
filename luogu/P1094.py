import sys


def main():
    buffered = list(map(int, sys.stdin.buffer.read().strip().split()))
    w = buffered[0]
    n = buffered[1]
    p: list[int] = []
    for i in range(2, len(buffered)):
        p.append(buffered[i])

    p.sort()

    l, r, ans = 1, n - 1, 0

    # 直到左右相遇结束
    while l <= r:
        # 假如相加小于上限
        # 则消耗最便宜的(l++)
        if p[l] + p[r] <= w:
            l += 1
        # 假如超过，就只能选右边最贵的
        r -= 1
        # 无论组没组成队 单双都是一组的
        ans += 1

    print(ans)
    return


if __name__ == "__main__":
    main()
