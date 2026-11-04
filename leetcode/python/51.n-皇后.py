#
# @lc app=leetcode.cn id=51 lang=python3
#
# [51] N 皇后
#


# @lc code=start
class Solution:
    def solveNQueens(self, n: int) -> list[list[str]]:
        state = [["." for _ in range(n)] for _ in range(n)]
        # 列上皇后
        cols = [False] * n
        # 主次对角线上皇后
        # 对角线数量为 2n-1 根
        diags1 = [False] * (2 * n - 1)
        diags2 = [False] * (2 * n - 1)
        res = []
        self.backtrace(0, n, state, cols, diags1, diags2, res)
        return res

    def backtrace(
        self,
        # 现在正在搜索的行
        row: int,
        # n 是总行数
        n: int,
        # 全局状态
        state: list[list[str]],
        # 列 两条对角线上皇后
        cols: list[bool],
        # diags1 主对角线，左上到右下
        diags1: list[bool],
        diags2: list[bool],
        res: list[list[str]],
    ):
        if row == n:
            res.append(["".join(list(row)) for row in state])
            return
        for col in range(n):
            # 计算对角线坐标
            diag1 = col - row + n - 1
            diag2 = col + row
            # 假如三条线都没有皇后
            if not cols[col] and not diags1[diag1] and not diags2[diag2]:
                # 落子
                state[row][col] = "Q"
                cols[col] = diags1[diag1] = diags2[diag2] = True
                self.backtrace(row + 1, n, state, cols, diags1, diags2, res)
                state[row][col] = "."
                cols[col] = diags1[diag1] = diags2[diag2] = False


# @lc code=end
if __name__ == "__main__":
    n = int(input())
    s = Solution().solveNQueens(n)
    for i in s:
        for j in i:
            print(j)
        print("\n")
