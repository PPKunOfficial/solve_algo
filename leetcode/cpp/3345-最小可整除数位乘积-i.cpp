/*
 * @lc app=leetcode.cn id=3345 lang=cpp
 *
 * [3345] 最小可整除数位乘积 I
 */

// @lc code=start
class Solution {
   public:
    int get_product(int n) {
        int m = n % 10;
        while (n / 10) {
            n /= 10;
            m *= n % 10;
        }
        return m;
    }
    int smallestNumber(int n, int t) {
        for (int i = n;; i++) {
            int c = get_product(i);
            if (c % t)
                continue;
            else
                return i;
        }
    }
};
// @lc code=end

int main() {
    auto s = Solution();
    s.smallestNumber(15, 3);
    return 0;
}