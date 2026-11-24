import sys


def main():
    n = int(sys.stdin.buffer.readline())
    full = (1 << n) - 1
    out = []
    cnt = 0

    def dfs(cols, d1, d2, st):
        nonlocal cnt
        if cols == full:
            cnt += 1
            if len(out) < 3:
                out.append(" ".join(map(str, st)))
            return
        avail = full & ~(cols | d1 | d2)
        while avail:
            bit = avail & -avail
            avail ^= bit
            st.append(bit.bit_length())  # 1-based：bit_length 即 col+1
            dfs(cols | bit, ((d1 | bit) << 1) & full, (d2 | bit) >> 1, st)
            st.pop()

    dfs(0, 0, 0, [])

    for s in out:
        print(s)
    print(cnt)


main()
