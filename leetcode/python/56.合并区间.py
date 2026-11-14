class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        if not intervals:
            return []

        intervals.sort(key=lambda x: x[0])
        res = [intervals[0][:]]

        # 把结果数组的最后一个区间和当前区间比较
        for start, end in intervals[1:]:
            # 能合并就更新最后一个区间的右端点，不能合并就追加当前区间
            if start <= res[-1][1]:
                res[-1][1] = max(res[-1][1], end)
            else:
                res.append([start, end])

        return res
