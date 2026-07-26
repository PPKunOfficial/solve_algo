/*
 * @lc app=leetcode.cn id=2942 lang=rust
 *
 * [2942] 查找包含给定字符的单词
 */
pub struct Solution;
// @lc code=start
impl Solution {
    pub fn find_words_containing(words: Vec<String>, x: char) -> Vec<i32> {
        words
            .iter()
            .enumerate()
            .filter(|(_, word)| word.contains(x))
            .map(|(index, _)| index as i32)
            .collect()
    }
}
// @lc code=end
fn main() {}
