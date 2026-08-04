/*
 * @lc app=leetcode.cn id=3731 lang=cpp
 *
 * [3731] 找出缺失的元素
 */

// @lc code=start
#include <algorithm>
#include <unordered_set>
#include <vector>
using namespace std;

class Solution {
   public:
    vector<int> findMissingElements(vector<int>& nums) {
        vector<int> missing;
        if (nums.empty())
            return missing;
        int minVal = *min_element(nums.begin(), nums.end());
        int maxVal = *max_element(nums.begin(), nums.end());

        unordered_set<int> exist(nums.begin(), nums.end());

        for (int num = minVal; num <= maxVal; ++num) {
            if (exist.find(num) == exist.end()) {
                missing.push_back(num);
            }
        }
        return missing;
    }
};
// @lc code=end
