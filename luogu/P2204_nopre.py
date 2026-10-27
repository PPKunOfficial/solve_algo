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

    tot_value_np: float = 0
    for i in golds:
        single_weight = i[0]
        single_value = i[1]

        if single_weight > t:
            mv_rate = i[2]
            tot_value_np += float(mv_rate * t)
            break

        tot_value_np+=single_value
        t-=single_weight

    print("%.2f" % tot_value_np)


if __name__ == "__main__":
    main()
