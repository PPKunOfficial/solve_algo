/*
 * @lc app=leetcode.cn id=4 lang=rust
 *
 * [4] 寻找两个正序数组的中位数
 */
pub struct Solution;

// @lc code=start
impl Solution {
    pub fn find_median_sorted_arrays(nums1: Vec<i32>, nums2: Vec<i32>) -> f64 {
        if nums1.len() > nums2.len() {
            return Self::find_median_sorted_arrays(nums2, nums1);
        }

        let (s1n, s2n) = (nums1.len(), nums2.len());
        let (mut left, mut right) = (0, s1n);
        let half_l = (s1n + s2n + 1) / 2;

        while left <= right {
            let i = (left + right) / 2;
            let j = half_l - i;

            let nums1_l_max = if i == 0 { i32::MIN } else { nums1[i - 1] };
            let nums1_r_min = if i == s1n { i32::MAX } else { nums1[i] };
            let nums2_l_max = if j == 0 { i32::MIN } else { nums2[j - 1] };
            let nums2_r_min = if j == s2n { i32::MAX } else { nums2[j] };

            if nums1_l_max <= nums2_r_min && nums2_l_max <= nums1_r_min {
                let max_left = nums1_l_max.max(nums2_l_max) as f64;
                if (s1n + s2n) % 2 == 1 {
                    return max_left;
                } else {
                    let min_right = nums1_r_min.min(nums2_r_min) as f64;
                    return (max_left + min_right) / 2.0;
                }
            } else if nums1_l_max > nums2_r_min {
                right = i - 1;
            } else {
                left = i + 1;
            }
        }

        0.0
    }
}
// @lc code=end
fn main() {}
