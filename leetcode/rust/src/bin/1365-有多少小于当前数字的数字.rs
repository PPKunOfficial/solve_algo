/*
 * @lc app=leetcode.cn id=1365 lang=rust
 *
 * [1365] 有多少小于当前数字的数字
 */
pub struct Solution;
// @lc code=start
impl Solution {
    pub fn smaller_numbers_than_current(nums: Vec<i32>) -> Vec<i32> {
        nums.iter()
            .map(|&x| nums.iter().filter(|&&y| y < x).count() as i32)
            .collect()
    }
}
// @lc code=end

fn main() {}
