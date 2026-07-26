/*
 * @lc app=leetcode.cn id=448 lang=rust
 *
 * [448] 找到所有数组中消失的数字
 */
pub struct Solution;
// @lc code=start
use std::collections::HashSet;
impl Solution {
    pub fn find_disappeared_numbers(nums: Vec<i32>) -> Vec<i32> {
        let n = nums.len() as i32;
        let hash_nums: HashSet<i32> = nums.into_iter().collect();
        (1..=n).filter(|x| !hash_nums.contains(x)).collect()
    }
}
// @lc code=end
fn main() {}
