/*
 * @lc app=leetcode.cn id=448 lang=rust
 *
 * [448] 找到所有数组中消失的数字
 */
pub struct Solution;
// @lc code=start
impl Solution {
    pub fn find_disappeared_numbers(mut nums: Vec<i32>) -> Vec<i32> {
        // 签到表式

        (0..nums.len()).for_each(|i| {
            let index = (nums[i].abs() as usize) - 1;
            nums[index] = -nums[index].abs();
        });

        nums.into_iter()
            .enumerate()
            .filter_map(|(i, num)| if num > 0 { Some((i + 1) as i32) } else { None })
            .collect()
    }
}
// @lc code=end
fn main() {
    println!(
        "{:?}",
        Solution::find_disappeared_numbers(vec![4, 3, 2, 7, 8, 2, 3, 1])
    )
}
