from re import sub
import sys


def main():
    buffered = list(map(int, sys.stdin.read().split()))
    n, m = buffered[0], buffered[1]
    matrix = [[i * n + j + 1 for j in range(n)] for i in range(n)]
    scarlets = []
    for i in range(2, m * 4 + 2, 4):
        scarlets.append(
            (buffered[i], buffered[i + 1], buffered[i + 2], buffered[i + 3])
        )
    del buffered

    for x, y, r, z in scarlets:
        rotate_matrix(matrix, x, y, r, z)

    out = "\n".join(" ".join(map(str, row)) for row in matrix)
    print(out)
    return


def rotate_matrix(mt, x, y, r, z):
    x -= 1
    y -= 1
    s = 2 * r + 1

    # sub_matrix = [[0] * (2 * r + 1)] * (2 * r + 1) 浅拷贝！
    # 先把子矩阵复制出来，避免边读边写互相覆盖
    sub = [[mt[x - r + i][y - r + j] for j in range(s)] for i in range(s)]

    for i in range(s):
        for j in range(s):
            if z == 0:
                ni, nj = j, s - 1 - i  # 顺时针
            else:
                ni, nj = s - 1 - j, i  # 逆时针
            mt[x - r + ni][y - r + nj] = sub[i][j]


if __name__ == "__main__":
    main()
