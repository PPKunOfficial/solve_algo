import sys


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
    for idx, (i, _) in enumerate(ministers):
        pre_plus_left_hand.append(pre_plus_left_hand[idx] * i)

    ministers_award: list[int] = []
    for i in range(1, len(pre_plus_left_hand)):
        ministers_award.append(pre_plus_left_hand[i - 1] // ministers[i - 1][1])

    print(max(ministers_award))
    return


if __name__ == "__main__":
    main()
