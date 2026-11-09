class Solution:
    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        left=0
        sum=0 # 窗口内总和
        n=len(nums)
        ans=n+1

        for r in range(len(nums)):
            sum+=nums[r] # 右指针进窗口
            while sum>=target: # 窗口总和过大
                ans=min(ans,r-left+1)
                sum-=nums[left]
                left+=1 # 左指针后移，减少窗口内的数，让窗口长度尽可能小

        return 0 if ans == n+1 else ans
