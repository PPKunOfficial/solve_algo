/*
 * @lc app=leetcode.cn id=877 lang=cpp
 *
 * [877] 石子游戏
 */

// @lc code=start
#include <algorithm>
#include <iostream>
#include <vector>
class Solution {
   public:
    bool stoneGame(std::vector<int>& piles) {
        int n = piles.size();
        std::vector<std::vector<int>> dp(n, std::vector<int>(n, 0));
        for (int i = 0; i < n; i++)
            dp[i][i] = piles[i];

        for (int len = 2; len <= n; len++) {
            for (int i = 0; i <= n - len; i++) {
                int j = i + len - 1;

                dp[i][j] =
                    std::max(piles[i] - dp[i + 1][j], piles[j] - dp[i][j - 1]);
            }
        }
        return dp[0][n - 1] > 0;
    }
};
// @lc code=end

int main() {
    auto s = Solution();
    std::vector<int> p = {1, 5, 2};
    std::cout << s.stoneGame(p);
    return 0;
}