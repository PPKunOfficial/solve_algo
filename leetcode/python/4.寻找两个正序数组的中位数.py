#
# @lc app=leetcode.cn id=4 lang=python3
#
# [4] 寻找两个正序数组的中位数
#


# @lc code=start
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:

        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1

        s1n, s2n = len(nums1), len(nums2)
        l, r = 0, s1n
        half_l = (s1n + s2n + 1) // 2

        while l <= r:
            i = (l + r) // 2
            j = half_l - i

            nums1LMax = float("-inf") if i == 0 else nums1[i - 1]
            nums1RMin = float("inf") if i == s1n else nums1[i]
            nums2LMax = float("-inf") if j == 0 else nums2[j - 1]
            nums2RMin = float("inf") if j == s2n else nums2[j]
            if nums1LMax <= nums2RMin and nums2LMax <= nums1RMin:
                return (
                    float(max(nums1LMax, nums2LMax))
                    if (s1n + s2n) % 2 == 1
                    else float(
                        (max(nums1LMax, nums2LMax) + min(nums1RMin, nums2RMin)) / 2
                    )
                )
            elif nums1LMax > nums2RMin:
                r = i - 1
            else:
                l = i + 1

        return 0.0


# @lc code=end

nums1, nums2 = [1, 3], [2]
s = Solution()
print(s.findMedianSortedArrays(nums1, nums2))
