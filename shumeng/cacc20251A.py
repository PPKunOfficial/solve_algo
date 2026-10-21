n, m = map(int, input().split())
p = list(range(1, n + 1))

idx = 0

while len(p) > 1:
    idx = (idx + m - 1) % len(p)
    p.pop(idx)

    if idx == len(p):
        idx = 0

print(p[0])