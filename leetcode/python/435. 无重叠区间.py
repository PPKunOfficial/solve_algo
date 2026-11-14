class Solution:
    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        if not intervals:
            return 0

        intervals.sort(key=lambda x: x[0])
        tot = 0
        last_end = intervals[0][1]  # 只需记住保留区间的右端点

        for start, end in intervals[1:]:
            if start < last_end:
                tot += 1
                last_end = min(last_end, end)  # 保留右端点更小的那个
            else:
                last_end = end

        return tot


sol = Solution()
intervals = [[1, 100], [11, 22], [1, 11], [2, 12]]
print(sol.eraseOverlapIntervals(intervals))
