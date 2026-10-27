from fractions import Fraction
import sys
import bisect


def main():
    n, t = map(int, sys.stdin.readline().split())

    # m v 出金率
    golds: list[tuple[int, int, Fraction]] = []

    for _ in range(n):
        a, b = map(int, sys.stdin.readline().split())
        golds.append((a, b, Fraction(b, a)))

    golds.sort(key=lambda x: x[2], reverse=True)

    pre_value: list[int] = [0] * (n + 1)
    pre_weight: list[int] = [0] * (n + 1)

    for i in range(0, n):
        m, v, _ = golds[i]
        pre_value[i + 1] = pre_value[i] + v
        pre_weight[i + 1] = pre_weight[i] + m

    if pre_weight[n] <= t:
        print("%.2f" % pre_value[n])
        return

    max_value_step = bisect.bisect_right(pre_weight, t) - 1
    extra_weight = t - pre_weight[max_value_step]
    tot_value: float | int = float(golds[max_value_step][2] * extra_weight) + pre_value[max_value_step]

    print("%.2f" % tot_value)


if __name__ == "__main__":
    main()
