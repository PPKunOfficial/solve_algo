import bisect
import sys


def main():
    buffered = list(map(int, sys.stdin.buffer.read().split()))
    n, m = buffered[0], buffered[1]
    nums = buffered[2 : 2 + n]
    psrc = buffered[2 + n : 2 + n + m]
    del buffered
    for i in psrc:
        f = bisect.bisect_left(nums, i)
        # 查看是否越界 and 当前找到的元素是否是他本身
        if f < n and nums[f] == i:
            print(f + 1, end=" ")
        else:
            print(-1, end=" ")


if __name__ == "__main__":
    main()
