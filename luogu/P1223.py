import sys

n = int(input())
t = [(i + 1, t) for i, t in enumerate(map(int, sys.stdin.readline().split()))]

t.sort(key=lambda x: (x[1], x[0]))

total_wait = 0
cur_time = 0
order = []

for idx, time in t:
    order.append(str(idx))
    total_wait += cur_time
    cur_time += time

print(" ".join(order))
print(f"{total_wait / n:.2f}")
