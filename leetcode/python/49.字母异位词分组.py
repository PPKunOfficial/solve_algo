#
# @lc app=leetcode.cn id=49 lang=python3
#
# [49] 字母异位词分组
#

# @lc code=start
class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        anagrams = {}
        for s in strs:
            key = ''.join(sorted(s))
            if key not in anagrams:
                anagrams[key] = []
            anagrams[key].append(s)
        return list(anagrams.values())
        
# @lc code=end

# eat -> aet tea -> aet
# {"aet":["eat","tea","ate"]}
# 输出 -> [["eat","tea","ate"],.....]

Solution().groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"])