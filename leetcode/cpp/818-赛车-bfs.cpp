/*
 * @lc app=leetcode.cn id=818 lang=cpp
 *
 * [818] 赛车
 */

// @lc code=start
#include <queue>
#include <string>
#include <unordered_set>
#include <utility>
class Solution {
   public:
    int racecar(int target) {
        // 初始状态 {位置，速度}
        std::queue<std::pair<int, int>> q;
        q.push({0, 1});

        std::unordered_set<std::string> visited;
        visited.insert("0,1");

        int steps = 0;
        while (!q.empty()) {
            int size = q.size();

            for (int i = 0; i < size; ++i) {
                auto [pos, speed] = q.front();
                q.pop();

                if (pos == target)
                    return steps;

                // 下一步是 A
                int next_posA = pos + speed;
                int next_spedA = speed * 2;
                if (next_posA > 0 && next_posA < 1.5 * target) {
                    std::string key = std::to_string(next_posA) + "," + std::to_string(next_spedA);
                    if (!visited.count(key)) {
                        visited.insert(key);
                        q.push({next_posA, next_spedA});
                    }
                }

                // 下一步是 R
                int next_posR = pos;
                int next_spedR = speed > 0 ? -1 : 1;
                if (next_posR > 0 && next_posR < 1.5 * target) {
                    std::string key = std::to_string(next_posR) + "," + std::to_string(next_spedR);
                    if (!visited.count(key)) {
                        visited.insert(key);
                        q.push({next_posR, next_spedR});
                    }
                }
            }
            steps++;
        }
        return -1;
    }
};
// @lc code=end

int main() {
    auto s = Solution();
    s.racecar(6);
    return 0;
}