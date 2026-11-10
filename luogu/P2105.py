import sys


def main():
    n, m, k = map(int, sys.stdin.readline().split())
    queens: list[tuple[int, int]] = []
    for _ in range(k):
        x, y = map(int, sys.stdin.readline().split())
        x -= 1
        y -= 1
        queens.append((x, y))

    return


if __name__ == "__main__":
    main()
