import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    k = next(it)
    a = [next(it) for _ in range(n)]
    b = [next(it) for _ in range(n)]

    diff = [a[i] - b[i] for i in range(n)]
    diff.sort()

    # 贪色策略：
    # 先把全部打折后的总价加起来
    # 然后对比打折前后变化
    # 遍历变化，假如发现打折前总价更低了就选用（前提没到 k 件）
    total = sum(b)

    for i, d in enumerate(diff):
        if i < k or d < 0:
            total += d

    print(total)


if __name__ == "__main__":
    main()
