/*
 * @lc app=leetcode.cn id=3741 lang=rust
 *
 * [3741] 三个相等元素之间的最小距离 II
 */
pub struct Solution;
// @lc code=start
use std::collections::HashMap;
impl Solution {
    pub fn minimum_distance(nums: Vec<i32>) -> i32 {
        let pmap = nums
            .iter()
            .enumerate()
            .fold(HashMap::new(), |mut map, (index, num)| {
                map.entry(num).or_insert_with(Vec::new).push(index);
                map
            });
        pmap.values()
            .filter(|l| l.len() >= 3)
            .flat_map(|l| l.windows(3).map(|w| 2 * (w[2] - w[0])))
            .min()
            .map_or(-1, |ans| ans as i32)
    }
}
// @lc code=end
fn main() {}
