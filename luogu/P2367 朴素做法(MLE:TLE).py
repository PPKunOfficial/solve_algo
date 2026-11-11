import sys


# 这道题简单的朴素做法过不了，会爆内存和爆时间
def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, p = data[0], data[1]
    stu_score = data[2 : 2 + n]
    oper = data[2 + n : 2 + n + (p * 3)]
    del data

    for i in range(0, len(oper), 3):
        x, y, z = oper[i], oper[i + 1], oper[i + 2]
        for j in range(x - 1, y):
            stu_score[j] += z
    del oper
    print(min(stu_score))


if __name__ == "__main__":
    main()
