def main():
    n = int(input())
    cols = [False] * n
    diags1 = [False] * (2 * n - 1)
    diags2 = [False] * (2 * n - 1)

    res = []
    st = [0] * n

    def dfs(row: int):
        if row == n:
            res.append(st.copy())
            return
        for col in range(n):
            # 判断列 对角线上后
            diag1 = col - row + n - 1
            diag2 = col + row
            if cols[col] or diags1[diag1] or diags2[diag2]:
                continue
            else:
                diags1[diag1] = diags2[diag2] = cols[col] = True
                st[row] = col
                dfs(row + 1)
                diags1[diag1] = diags2[diag2] = cols[col] = False

    dfs(0)
    for i in range(3):
        print(" ".join(str(x + 1) for x in res[i]))
    print(len(res))


main()
