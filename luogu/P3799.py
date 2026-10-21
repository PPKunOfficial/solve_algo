import sys

input_data = sys.stdin.read().split()
if not input_data:
    exit()

n = int(input_data[0])

MOD = 10**9 + 7
MAXV = 5000

cnt = [0]*(MAXV+1)
max_len = 0

for i in range(1, n+1):
    val = int(input_data[i])
    cnt[val] += 1
    if val > max_len:
        max_len = val

ans = 0


def c2(m: int):
    return m * (m - 1) // 2

for L in range(1,max_len+1):
    if cnt[L]<2:
        continue
    ways_L=c2(cnt[L])%MOD
    ways_split=0

    # 枚举组成第三条边的两个较短边：j 和 L - j
    for j in range(1, L // 2 + 1):
        k = L - j
        if j == k:
            # 两根短木棒长度相同
            if cnt[j] >= 2:
                ways_split = (ways_split + c2(cnt[j])) % MOD
        else:
            # 两根短木棒长度不同
            if cnt[j] > 0 and cnt[k] > 0:
                ways_split = (ways_split + cnt[j] * cnt[k]) % MOD

    ans = (ans + ways_L * ways_split) % MOD

print(ans)
