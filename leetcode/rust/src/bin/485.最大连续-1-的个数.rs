/*
 * @lc app=leetcode.cn id=485 lang=rust
 *
 * [485] 最大连续 1 的个数
 */
pub struct Solution;
// @lc code=start
impl Solution {
    pub fn find_max_consecutive_ones(nums: Vec<i32>) -> i32 {
        nums.into_iter()
            .fold((0, 0), |(curr, max), x| {
                if x == 1 {
                    (curr + 1, max.max(curr + 1))
                } else {
                    (0, max)
                }
            })
            .1
    }
}
// @lc code=end
fn main() {}
