import sys

n = int(input())
competitions = [tuple(map(int, sys.stdin.readline().split())) for _ in range(n)]

competitions.sort(key=lambda x: x[1])

tot = 0
last_ending = -1

for start, end in competitions:
    if start >= last_ending:
        tot += 1
        last_ending = end

print(tot)
