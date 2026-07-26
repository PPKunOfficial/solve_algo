/*
 * @lc app=leetcode.cn id=485 lang=rust
 *
 * [485] 最大连续 1 的个数
 */
pub struct Solution;
// @lc code=start
impl Solution {
    pub fn find_max_consecutive_ones(nums: Vec<i32>) -> i32 {
        nums.split(|&n| n == 0).map(|s| s.len()).max().unwrap_or(0) as i32
    }
}
// @lc code=end
fn main() {}
