import sys


def main():
    buffered = list(map(int, sys.stdin.read().split()))
    n, m = buffered[0], buffered[1]
    nums = buffered[2:]
    del buffered
    nums.sort()
    print(" ".join(map(str, nums)))
    return


if __name__ == "__main__":
    main()
