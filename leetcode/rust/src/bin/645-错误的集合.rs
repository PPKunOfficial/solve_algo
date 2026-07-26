/*
 * @lc app=leetcode.cn id=645 lang=rust
 *
 * [645] 错误的集合
 */
pub struct Solution;
// @lc code=start
impl Solution {
    pub fn find_error_nums(mut nums: Vec<i32>) -> Vec<i32> {
        nums.sort_unstable();
        let dup = nums
            .windows(2)
            .find(|w| w[0] == w[1])
            .map(|w| w[0])
            .unwrap();
        let sum: i32 = nums.iter().sum();
        let exp: i32 = (1..=nums.len() as i32).sum();
        vec![dup, exp - sum + dup]
    }
}
// @lc code=end
fn main() {
    println!("{:?}", Solution::find_error_nums(vec![2, 3, 2]));
}
