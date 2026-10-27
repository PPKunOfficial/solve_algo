import sys

n, x = map(int, input().split())
a = list(map(int, sys.stdin.readline().split()))

# 优先吃后一个，后一个吃完了再吃前一个
# 后一个对后续影响大，从而达到最优
bef = sum(a)
for i in range(len(a) - 1):
    sum_n = a[i] + a[i + 1]
    # 前后总和大于指定的
    if sum_n > x:
        e = sum_n - x
        ef = a[i + 1] - e
        if ef >= 0:
            a[i + 1] = a[i + 1] - e
        else:
            a[i + 1] = 0
            a[i] = a[i] + ef
print(bef - sum(a))
