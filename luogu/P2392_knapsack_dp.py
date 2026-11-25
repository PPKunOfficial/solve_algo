import sys


def knapsack():
    pass


def main():
    s = list(map(int, sys.stdin.buffer.readline().split()))
    ans = 0
    for _ in s:
        n = list(map(int, sys.stdin.buffer.readline().split()))

        # 01背包问题 尽可能把一边凑到total/2
        # 因为把一堆题交给两边并行，耗费时间决定于最长一边
        # 因此让两边尽量贴近则最快

        total_time = sum(n)
        half_time = total_time // 2
        dp = [0] * (half_time + 1)

        for t in n:
            for j in range(half_time, t - 1, -1):
                dp[j] = max(dp[j], dp[j - t] + t)

        ans += total_time - dp[half_time]

    print(ans)


main()
