import sys
from functools import cmp_to_key


def cmp(x, y):
    if x + y > y + x:
        return -1
    elif x + y < y + x:
        return 1
    else:
        return 0


def main():
    buffered = list(sys.stdin.read().split())
    n = int(buffered[0])
    a = buffered[1 : n + 1]

    a.sort(key=cmp_to_key(cmp))

    print("".join(a))
    return


if __name__ == "__main__":
    main()
