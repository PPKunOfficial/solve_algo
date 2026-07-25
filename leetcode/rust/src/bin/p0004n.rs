/*
 * @lc app=leetcode.cn id=4 lang=rust
 *
 * [4] 寻找两个正序数组的中位数
 */

pub struct Solution;

// @lc code=start
impl Solution {
    pub fn find_median_sorted_arrays(nums1: Vec<i32>, nums2: Vec<i32>) -> f64 {
        let search = |a: &[i32], b: &[i32]| -> f64 {
            let (m, n) = (a.len(), b.len());
            let half_len = (m + n + 1) / 2;

            let mut low = 0;
            let mut high = m + 1;

            while low < high {
                let i = low + (high - low) / 2;
                let j = half_len - i;

                if i == 0 || j >= n || a[i - 1] <= b[j] {
                    low = i + 1;
                } else {
                    high = i;
                }
            }

            let i = low - 1;
            let j = half_len - i;

            let a_left = if i == 0 { i32::MIN } else { a[i - 1] };
            let a_right = if i == m { i32::MAX } else { a[i] };
            let b_left = if j == 0 { i32::MIN } else { b[j - 1] };
            let b_right = if j == n { i32::MAX } else { b[j] };

            let max_left = a_left.max(b_left) as f64;
            if (m + n) % 2 == 1 {
                max_left
            } else {
                let min_right = a_right.min(b_right) as f64;
                (max_left + min_right) / 2.0
            }
        };

        if nums1.len() <= nums2.len() {
            search(&nums1, &nums2)
        } else {
            search(&nums2, &nums1)
        }
    }
}
// @lc code=end
fn main() {}
