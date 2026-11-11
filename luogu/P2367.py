import sys
from array import array

data = sys.stdin.buffer.read()
ptr = 0
L = len(data)


def next_int():
    global ptr
    while ptr < L and data[ptr] <= 32:
        ptr += 1
    sign = 1
    if data[ptr] == 45:
        sign = -1
        ptr += 1
    num = 0
    while ptr < L and data[ptr] > 32:
        num = num * 10 + (data[ptr] - 48)
        ptr += 1
    return sign * num


def main():
    n = next_int()
    p = next_int()

    diff = array("i", [0]) * (n + 1)
    prev = 0
    for i in range(n):
        v = next_int()
        if i == 0:
            diff[0] = v
        else:
            diff[i] = v - prev
        prev = v

    for _ in range(p):
        x = next_int()
        y = next_int()
        z = next_int()
        diff[x - 1] += z
        diff[y] -= z

    cur = 0
    ans = 1 << 30
    for i in range(n):
        cur += diff[i]
        ans = min(cur, ans)

    sys.stdout.write(str(ans))


main()
