#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const int dx[] = {1, 1, 2, 2, -1, -1, -2, -2};
const int dy[] = {2, -2, 1, -1, 2, -2, 1, -1};

int main(void) {
    int n, m, cx, cy;
    if (scanf("%d %d %d %d", &n, &m, &cx, &cy) != 4)
        return 0;

    bool** is_blocked = (bool**)malloc(sizeof(bool*) * (n + 1));
    for (int i = 0; i <= n; i++) {
        is_blocked[i] = (bool*)malloc(sizeof(bool) * (m + 1));
        memset(is_blocked[i], 0, sizeof(bool) * (m + 1));
    }

    is_blocked[cx][cy] = 1;

    for (int i = 0; i < 8; i++) {
        int x = cx + dx[i];
        int y = cy + dy[i];
        if (x >= 0 && y >= 0 && x <= n && y <= m)
            is_blocked[x][y] = 1;
    }

    long long** dp = (long long**)malloc(sizeof(long long*) * (n + 1));
    for (int i = 0; i <= n; i++) {
        dp[i] = (long long*)malloc(sizeof(long long) * (m + 1));
        memset(dp[i], 0, sizeof(long long) * (m + 1));
    }

    if (!is_blocked[0][0])
        dp[0][0] = 1;

    // 填表
    for (int i = 0; i <= n; i++) {
        for (int j = 0; j <= m; j++) {
            if (i == 0 && j == 0)
                continue;
            // 马能吃到喵
            if (is_blocked[i][j])
                dp[i][j] = 0;
            else {
                // 把左边过来的路径+上面过来的路径就是可以到达这里的路径喵
                long long from_left = (i > 0) ? dp[i - 1][j] : 0;
                long long from_up = (j > 0) ? dp[i][j - 1] : 0;
                dp[i][j] = from_left + from_up;
            }
        }
    }
    printf("%lld", dp[n][m]);

    for (int i = 0; i <= n; i++) {
        free(is_blocked[i]);
        free(dp[i]);
    }
    free(is_blocked);
    free(dp);
    return 0;
}