import sys


def main():
    n = int(input())
    men = list(map(int, sys.stdin.readline().split()))
    m = int(input())
    women = list(map(int, sys.stdin.readline().split()))

    men.sort()
    women.sort()
    np = 0
    mp = 0
    ans = 0
    for i in range(max(n, m)):
        # 判断是否符合水平
        if men[np] == women[mp]:
            ans += 1
    return


if __name__ == "__main__":
    main()
