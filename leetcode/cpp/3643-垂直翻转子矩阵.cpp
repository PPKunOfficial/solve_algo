/*
 * @lc app=leetcode.cn id=3643 lang=cpp
 *
 * [3643] 垂直翻转子矩阵
 */

// @lc code=start
#include <utility>
#include <vector>
using namespace std;
class Solution {
   public:
    vector<vector<int>> reverseSubmatrix(vector<vector<int>>& grid, int x,
                                         int y, int k) {
        for (int r = 0; r < k / 2; ++r) {
            int top = x + r;
            int bottom = x + k - 1 - r;
            for (int c = y; c < y + k; ++c) {
                swap(grid[top][c], grid[bottom][c]);
            }
        }
        return grid;
    }
};
// @lc code=end
int main() {
    auto s = Solution();
    std::vector<std::vector<int>> vec = {{3, 4, 2, 3}, {2, 3, 4, 2}};

    auto v = s.reverseSubmatrix(vec, 0, 2, 2);
    return 0;
}