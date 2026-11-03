import sys


def main():
    n = int(input().strip())
    scores: list[tuple[int, int, int, int, int]] = []
    for i in range(n):
        c, m, e = map(int, sys.stdin.readline().split())
        scores.append((i + 1, c, m, e, c + m + e))
    scores.sort(key=lambda x: (-x[4], -x[1], x[0]))
    js = 0
    for i, _, _, _, t in scores:
        print(i, t)
        js += 1
        if js >= 5:
            break
    return


if __name__ == "__main__":
    main()
