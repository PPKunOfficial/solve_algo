class Solution:
    height: list[int]

    def calc_water(self, l: int, r: int):
        length = r - l
        lh, rh = self.height[l], self.height[r]
        return length * min(lh, rh)

    def maxArea(self, height: list[int]) -> int:
        self.height = height
        l, r = 0, len(height) - 1
        max_water = 0
        while l <= r:
            now_water = self.calc_water(l, r)
            max_water = max(now_water, max_water)

            # 矮的那边挪一下
            if height[l] > height[r]:
                r -= 1
            else:
                l += 1

        return max_water
