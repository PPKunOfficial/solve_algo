/*
 * @lc app=leetcode.cn id=818 lang=rust
 *
 * [818] 赛车
 */

pub struct Solution;

// @lc code=start
use std::cmp;
impl Solution {
    pub fn racecar(target: i32) -> i32 {
        let target = target as usize;
        let mut dp = vec![0; target + 1];
        for i in 1..=target {
            let k = (i + 1).next_power_of_two().trailing_zeros() as u32;

            // 步数对应所走距离 2^k-1
            let distance_k = 2_usize.pow(k) - 1;

            // 恰好到达
            if distance_k == i {
                dp[i] = k;
                continue;
            }

            // 掉头
            // 距离=当前 A + 1 次 R 掉头完所处地方到达目标所需步数
            dp[i] = k + 1 + dp[2_usize.pow(k) - 1 - i];

            for j in 0..(k - 1) {
                let rd = i - (2_usize.pow(k - 1) - 1) + (2_usize.pow(j) - 1);
                dp[i] = cmp::min(dp[i], (k - 1) + 1 + j + 1 + dp[rd]);
            }
        }
        dp[target] as i32
    }
}
// @lc code=end

fn main() {}
