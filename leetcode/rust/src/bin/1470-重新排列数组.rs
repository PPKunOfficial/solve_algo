/*
 * @lc app=leetcode.cn id=1470 lang=rust
 *
 * [1470] 重新排列数组
 */
pub struct Solution;
// @lc code=start
impl Solution {
    pub fn shuffle(nums: Vec<i32>, n: i32) -> Vec<i32> {
        let n = n as usize;

        // 数组长是 2n，借用前半和后半所以是 ..n 和 n..
        nums[..n]
            .iter()
            .zip(&nums[n..])
            .flat_map(|(&x, &y)| [x, y])
            .collect()
    }
}
// @lc code=end

fn main() {}
