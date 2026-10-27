import heapq
import sys


def main():
    input = sys.stdin.readline

    n = int(input())
    fruits = list(map(int, input().split()))

    if n == 1:
        print(0)
        return

    heapq.heapify(fruits)

    ans = 0

    while len(fruits) > 1:
        a = heapq.heappop(fruits)
        b = heapq.heappop(fruits)

        cost = a + b
        ans += cost

        heapq.heappush(fruits, cost)

    print(ans)


if __name__ == "__main__":
    main()
