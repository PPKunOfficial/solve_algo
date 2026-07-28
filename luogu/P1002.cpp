#include <iostream>
#include <vector>

const int dx[] = {1, 1, 2, 2, -1, -1, -2, -2};
const int dy[] = {2, -2, 1, -1, 2, -2, 1, -1};

int main() {
    // B 点目标，马(C) 位置
    int n, m, cx, cy;
    if (!(std::cin >> n >> m >> cx >> cy))
        return 0;

    // 标记马和可到达的八个位置
    std::vector<std::vector<bool>> is_blocked(n + 1,
                                              std::vector<bool>(m + 1, false));
    is_blocked[cx][cy] = 1;

    for (int i = 0; i < 8; i++) {
        int nx = cx + dx[i];
        int ny = cy + dy[i];
        if (nx >= 0 && nx <= n && ny >= 0 && ny <= m)
            is_blocked[nx][ny] = 1;
    }

    std::vector<std::vector<long long>> dp(n + 1,
                                           std::vector<long long>(m + 1, 0));
    if (!is_blocked[0][0]) {
        dp[0][0] = 1;
    }

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
    std::cout << dp[n][m];
    return 0;
}