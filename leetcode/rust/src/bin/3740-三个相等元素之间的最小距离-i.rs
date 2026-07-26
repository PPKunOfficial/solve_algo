/*
 * @lc app=leetcode.cn id=3740 lang=rust
 *
 * [3740] 三个相等元素之间的最小距离 I
 */
pub struct Solution;
// @lc code=start
impl Solution {
    pub fn minimum_distance(nums: Vec<i32>) -> i32 {
        let find_next = |nums: Vec<i32>, index: usize, target: i32| -> Option<usize> {
            for i in index..nums.len() {
                if nums[i] == target {
                    return Some(i);
                }
            }
            None
        };
        let mut length = usize::MAX;
        for (index, num) in nums.iter().enumerate() {
            let find_first = find_next(nums.clone(), index + 1, *num);
            if find_first.is_some() {
                let find_second = find_next(nums.clone(), find_first.unwrap() + 1, *num);
                if find_second.is_some() {
                    let now_length = (find_first.unwrap() - index)
                        + (find_second.unwrap() - find_first.unwrap())
                        + (find_second.unwrap() - index);
                    if now_length < length {
                        length = now_length;
                    }
                }
            }
        }
        length as i32
    }
}
// @lc code=end
fn main() {
    println!("{:?}", Solution::minimum_distance(vec![1, 2, 1, 1, 3]));
}
