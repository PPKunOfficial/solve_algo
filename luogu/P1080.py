import sys

"""
相邻项比较
![P1080 数学](luogu/P1080 数学部分.png)
"""


def main():
    buffered = list(map(int, sys.stdin.buffer.read().split()))
    n = buffered[0]
    king_left_hand, king_right_hand = buffered[1], buffered[2]
    ministers: list[tuple[int, int]] = []

    pre_plus_left_hand: list[int] = []
    pre_plus_left_hand.append(king_left_hand)
    for i in range(3, 3 + 2 * n, 2):
        ministers.append((buffered[i], buffered[i + 1]))
    ministers.sort(key=lambda x: x[0] * x[1], reverse=False)

    prod = king_left_hand
    ans = 0
    for a, b in ministers:
        coins = prod // b
        if coins > ans:
            ans = coins
        prod *= a

    print(ans)
    return


if __name__ == "__main__":
    main()
