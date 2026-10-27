import bisect
import sys


def main():
    # 读入数据
    inbuffer = list(map(int, sys.stdin.buffer.read().split()))
    n, s, a, b = map(int, inbuffer[0:4])
    max_high = a + b
    apples: list[tuple[int, int]] = []
    for i in range(4, len(inbuffer), 2):
        apples.append((inbuffer[i], inbuffer[i + 1]))

    apples.sort(key=lambda x: (x[0], x[1]))

    hi = bisect.bisect_right(apples, (max_high, float("inf")))
    available_apples = apples[:hi]

    available_apples.sort(key=lambda x: x[1])

    tot_apples = 0
    for i, x in available_apples:
        s = s - x
        if s >= 0:
            tot_apples = tot_apples + 1

    print(tot_apples)


if __name__ == "__main__":
    main()
