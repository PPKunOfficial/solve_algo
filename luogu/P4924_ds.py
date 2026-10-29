import sys


def rotate(mt, x, y, r, z):
    """x, y 已经是 0-indexed 的中心，z=0 顺，z=1 逆"""
    x0 = x - r
    y0 = y - r
    s1 = 2 * r
    for i in range(r):
        for j in range(i, s1 - i):
            a_r, a_c = x0 + i, y0 + j
            if z == 0:  # 顺时针
                b_r, b_c = x0 + j, y0 + (s1 - i)
                c_r, c_c = x0 + (s1 - i), y0 + (s1 - j)
                d_r, d_c = x0 + (s1 - j), y0 + i
            else:  # 逆时针
                b_r, b_c = x0 + (s1 - j), y0 + i
                c_r, c_c = x0 + (s1 - i), y0 + (s1 - j)
                d_r, d_c = x0 + j, y0 + (s1 - i)

            temp = mt[a_r][a_c]
            mt[a_r][a_c] = mt[d_r][d_c]
            mt[d_r][d_c] = mt[c_r][c_c]
            mt[c_r][c_c] = mt[b_r][b_c]
            mt[b_r][b_c] = temp


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, m = data[0], data[1]

    # 初始化矩阵：尽量避免存很多不同的 int 对象
    matrix = [[i * n + j + 1 for j in range(n)] for i in range(n)]

    idx = 2
    for _ in range(m):
        x = data[idx] - 1
        y = data[idx + 1] - 1
        r = data[idx + 2]
        z = data[idx + 3]
        idx += 4
        rotate(matrix, x, y, r, z)

    out = "\n".join(" ".join(map(str, row)) for row in matrix)
    sys.stdout.write(out)


if __name__ == "__main__":
    main()
