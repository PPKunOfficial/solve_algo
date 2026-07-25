/*
 * @lc app=leetcode.cn id=1 lang=rust
 *
 * [1] 两数之和
 */

// 本地 rust-analyzer 需要该类型；LeetCode 只提交 code start/end 之间的代码。
pub struct Solution;

// @lc code=start
use std::collections::HashMap;
impl Solution {
    pub fn two_sum(nums: Vec<i32>, target: i32) -> Vec<i32> {
        let mut map = HashMap::new();
        nums.into_iter().enumerate().find_map(|(i, num)| {
            let c = target - num;
            if let Some(&prev_idx) = map.get(&c) {
                Some(vec![prev_idx as i32, i as i32])
            } else {
                map.insert(num as i32, i as i32)
                None
            }
        }).unwrap()
    }
}
// @lc code=end
