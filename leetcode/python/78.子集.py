class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        res = []
        path = []
        n = len(nums)

        def dfs(s):
            res.append(res)
            for i in range(s, n):
                path.append(nums[i])
                dfs(i + 1)
                path.pop()

        dfs(0)
        return res


sol = Solution()
sol.subsets(nums=[1, 2, 3])
