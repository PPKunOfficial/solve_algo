class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        m, n = len(grid), len(grid[0])
        ans = 0

        def dfs(i, j):
            # 越界和附近被水淹了就退出
            if i < 0 or i >= m or j < 0 or j >= n:
                return
            if grid[i][j] == "0":
                return

            # 不断向周围淹没，直到整个岛被淹没
            grid[i][j] = "0"

            dfs(i - 1, j)
            dfs(i + 1, j)
            dfs(i, j - 1)
            dfs(i, j + 1)

        # 找到下一个岛屿
        for i in range(m):
            for j in range(n):
                if grid[i][j] == "1":
                    ans += 1
                    dfs(i, j)

        return ans


sol = Solution()
print(
    sol.numIslands(
        grid=[
            ["1", "1", "1", "1", "0"],
            ["1", "1", "0", "1", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "0", "0", "0"],
        ]
    )
)
