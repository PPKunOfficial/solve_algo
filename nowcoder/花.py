import sys

MAGIC_MOD = 998244353

def main():
    t = int(sys.stdin.buffer.readline())
    for _ in range(t):
        n = int(sys.stdin.buffer.readline())
        a = list(map(int, sys.stdin.buffer.readline().split()))

        # 斐波那契递推
        fib_1 = fib_2 = 1

        # j循环递推
        q_prev1 = q_prev2 = 0
        prev_a = 0

        ans = 0
        for i in range(1, n + 1):
            aj = a[i - 1] % MAGIC_MOD
            ans = (ans + q_prev1 + aj * fib_2) % MAGIC_MOD
            qj = (q_prev1 + q_prev2 + prev_a) % MAGIC_MOD
            q_prev2, q_prev1 = q_prev1, qj
            prev_a = aj
            fib_1, fib_2 = fib_2, (fib_1 + fib_2) % MAGIC_MOD
        print(ans)

main()
