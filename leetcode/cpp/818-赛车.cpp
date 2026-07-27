/*
 * @lc app=leetcode.cn id=818 lang=cpp
 *
 * [818] 赛车
 */

// @lc code=start
#include <algorithm>
#include <cmath>
#include <vector>
class Solution {
   public:
    int get_k(int i) {
        int k = 0;
        while (pow(2, k) - 1 < i) {
            k++;
        }
        return k;
    }
    int racecar(int target) {
        std::vector<int> dp(target + 1, 0);
        for (int i = 1; i <= target; i++) {
            int k = get_k(i);

            // 恰好到达
            if (pow(2, k) - 1 == i) {
                dp[i] = k;
                continue;
            }

            // 掉头回来
            dp[i] = k + 1 + dp[pow(2, k) - 1 - i];

            for (int j = 0; j < k - 1; ++j) {
                int rdist = i - (pow(2, k - 1) - 1) + (pow(2, j) - 1);
                dp[i] = std::min(dp[i], (k - 1) + 1 + j + 1 + dp[rdist]);
            }
        }
        return dp[target];
    }
};
// @lc code=end
int main() { return 0; }