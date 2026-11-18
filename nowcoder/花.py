import sys

# ============ 本地测试开关 ============
USE_FILE = False  # 本地测试设 True；提交 OJ 时改成 False
INPUT_FILE = "/Users/pp/projects/solve_q/input.txt"
OUTPUT_FILE = "/Users/pp/projects/solve_q/output.txt"
# =====================================

if USE_FILE:
    sys.stdin = open(INPUT_FILE, "r")
    # sys.stdout = open(OUTPUT_FILE, "w")

fib = [1] * (10**6 + 1)

def f(x, y, z):
    if z == 1:
        return x
    if z == 2:
        return y
    if z >= 3:
        print(f"f: {fib[z - 2]} {fib[z - 1]}")
        return (fib[z - 2] * x + fib[z - 1] * y) % 998244353

    return 0

def fibg():
    for i in range(3, len(fib)):
        fib[i] = (fib[i - 1] + fib[i - 2]) % 998244353

def main():
    fibg()
    t = int(sys.stdin.buffer.readline())
    for _ in range(t):
        n = int(sys.stdin.buffer.readline())
        a = list(map(int, sys.stdin.buffer.readline().split()))
        tot = 0
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                r = f(a[i - 1], a[j - 1], j - i + 1)
                tot += r
                print(f"main: {(i, j, j - i + 1)} {r} {tot}")

        print(tot % 998244353)

main()

if USE_FILE:
    sys.stdout.close()
