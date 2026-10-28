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

    # 旋转
    for (
        x,
        y,
        r,
        z,
    ) in scarlets:
        x -= 1
        y -= 1

    return


def rotate_matrix(mt, x, y, r, z):
    x -= 1
    y -= 1
    # sub_matrix = [[0] * (2 * r + 1)] * (2 * r + 1) 浅拷贝！
    sub_matrix = [[0] * (2 * r + 1) for _ in range(2 * r + 1)]

    m, j = 0, 0
    for i in range(y - r, y + r + 1):
        for k in range(x - r, x + r + 1):
            sub_matrix[m][j] = matrix[i][k]
            j += 1
        j = 0
        m += 1
    del m, j

    # 顺时针旋转
    mid=r
    s=2*r+1
    if z==0:




    return sub_matrix


if __name__ == "__main__":
    n = 5
    matrix = [[i * n + j + 1 for j in range(n)] for i in range(n)]
    x, y, r, z = (2, 2, 1, 0)
    print(rotate_matrix(matrix, x, y, r, z))
