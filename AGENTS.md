# 动画项目约定

## Manim 题解命名

- Manim 动画脚本必须与对应 Rust 题解保持相同文件名，仅扩展名改为 `.py`。
  - Rust：`leetcode/rust/src/bin/1470-重新排列数组.rs`
  - Manim：`algorithm_explainer_video/leetcode/1470-重新排列数组.py`
- 已渲染成片必须命名为：`Leetcode力扣 {题号}. {题名}.mp4`。
  - 示例：`Leetcode力扣 448. 找到所有数组中消失的数字.mp4`
- 未经用户明确要求，不渲染仅进行重命名的动画脚本。
