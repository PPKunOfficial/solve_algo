import bisect

n, s = map(int, input().split())
soldiers: list = []

for i in range(n):
    c, p = map(int, input().split())
    soldiers.append((p,c))

soldiers.sort()

c_list = [c for c, _ in soldiers]

# 后缀和
suf_p = [0]*(n+1)
suf_pc = [0]*(n+1)

for i in range(n-1, -1, -1):
    c, p = soldiers[i]
    # 后缀和，上一个加当前的
    suf_p[i] = suf_p[i+1]+p
    suf_pc[i] = suf_pc[i+1]+p*c


def calc(t):
    pos = bisect.bisect_right(c_list, t)
    # 合练 + 训练的单价（不包含合练）- 已经练过所对应的价格
    return t*s+suf_pc[pos]-t*suf_p[pos]


ans = calc(0)
for c, _ in soldiers:
    ans = min(ans, calc(c))

print(ans)
