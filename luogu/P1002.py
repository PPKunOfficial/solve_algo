import sys

dx = [1, 1, 2, 2, -1, -1, -2, -2]
dy = [2, -2, 1, -1, 2, -2, 1, -1]


def main():
    n, m, cx, cy = map(int, sys.stdin.buffer.readline().split())

    is_blocked = [[False for _ in range(m + 1)] for _ in range(n + 1)]

    is_blocked[cx][cy] = True

    # 按照前面定义的马的攻击范围
    # 在这里进行预先标记
    for i in range(8):
        nx = cx + dx[i]
        ny = cy + dy[i]
        if 0 <= nx <= n and 0 <= ny <= m:
            is_blocked[nx][ny] = True

    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # 起始点初始化
    if not is_blocked[0][0]:
        dp[0][0] = 1

    for i in range(n + 1):
        for j in range(m + 1):
            # 起点已单独初始化，跳过
            if i == 0 and j == 0:
                continue
            # 假如这条路不能走，就下一个
            if is_blocked[i][j]:
                continue
            # 不然就把当前位置结果存进dp数组里
            # 当前位置可通行道路的总数
            # 左边+上面的数量
            left = dp[i - 1][j] if i > 0 else 0
            up = dp[i][j - 1] if j > 0 else 0
            dp[i][j] = left + up

    print(dp[n][m])


main()
