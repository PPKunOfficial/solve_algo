/*
 * @lc app=leetcode.cn id=5 lang=rust
 *
 * [5] 最长回文子串
 */
pub struct Solution;
// @lc code=start
impl Solution {
    pub fn longest_palindrome(s: String) -> String {
        let sb = s.as_bytes();
        let len = s.len();
        let expand_center = |mut l: usize, mut r: usize| -> (usize, usize) {
            while r < len && sb[l] == sb[r] {
                if l == 0 {
                    return (0, r - l + 1);
                }
                r += 1;
                l -= 1;
            }
            (l + 1, r - l - 1)
        };
        let (start, max_len) = (0..len)
            .flat_map(|i| [(i, i), (i, i + 1)])
            .map(|(l, r)| expand_center(l, r))
            .max_by_key(|&(_, length)| length)
            .unwrap_or((0, 0));
        s[start..start + max_len].to_string()
    }
}
// @lc code=end
fn main() {
    Solution::longest_palindrome("aba".to_string());
}
