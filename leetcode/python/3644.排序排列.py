#
# @lc app=leetcode.cn id=3644 lang=python3
#
# [3644] 排序排列
#

# @lc code=start
from typing import List


class Solution:
    def sortPermutation(self, nums: List[int]) -> int:
        ans =-1
        for i,x in enumerate(nums):
            if i != x:
                ans &= (i&x)

        return 0 if ans==-1 else ans


        
# @lc code=end

