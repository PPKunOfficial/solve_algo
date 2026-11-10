import sys


def main() -> int:
    n = int(input())
    tj_horse = list(map(int, sys.stdin.readline().split()))
    k_horse = list(map(int, sys.stdin.readline().split()))

    tj_horse.sort()
    k_horse.sort()

    # 最慢和最快的马
    i, j = 0, n - 1
    p, r = 0, n - 1
    ans = 0

    while i <= j:
        # 田忌的最快能跑过齐王的最快
        if tj_horse[j] > k_horse[r]:
            ans += 200
            j -= 1
            r -= 1
        elif tj_horse[j] < k_horse[r]:
            # 田忌最快跑不过齐王最快
            # 下等马战上等马
            ans -= 200
            r -= 1
            i += 1
        else:
            # 打平了
            # 田忌最慢比齐王最慢
            if tj_horse[i] > k_horse[p]:
                ans += 200
                i += 1
                p += 1
            else:
                if tj_horse[i] < k_horse[r]:
                    # 两个最慢比不过就用最慢比最快
                    ans -= 200
                # 不管打平还是输都是最慢对最快
                i += 1
                r -= 1
    print(ans)


if __name__ == "__main__":
    main()
