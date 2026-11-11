# ============================================================
# fastio.py —— Python 竞赛快读模板合集（含手动指针完整版）
# 用法：复制整个文件，在 main() 里取消注释你要的方案
# ============================================================
import re
import sys
from array import array

# ============================================================
# 方案 1：readline().split()  ——  通用首选
#   速度：★★★★     内存：低（一行）
#   适合：绝大多数题，数据分行良好
#   坑：单行 >10^6 个元素时 split 会炸内存
# ============================================================
readline = sys.stdin.buffer.readline


def read_pair():
    a, b = map(int, readline().split())
    return a, b


def read_list():
    return list(map(int, readline().split()))


# ============================================================
# 方案 2：read().split() + iter  ——  最快，适合小输入
#   速度：★★★★★    内存：高（全部输入 + split 列表）
#   适合：总整数 ≤ 10^6，内存 ≥ 256MB
# ============================================================
def load_all():
    it = iter(sys.stdin.buffer.read().split())

    def ni():
        return int(next(it))

    return ni


# ============================================================
# 方案 3：re.finditer 惰性  ——  大输入 + 省内存
#   速度：★★★★（C 扫描）    内存：原始输入大小
#   适合：单行元素极多 / 总整数 > 10^6
#   注意：PyPy 下 re 走 C bridge，可能比手写循环慢
# ============================================================
_NUM_RE = re.compile(rb"-?\d+")


def load_re():
    data = sys.stdin.buffer.read()
    gen = (int(m.group()) for m in _NUM_RE.finditer(data))

    def ni():
        return next(gen)

    return ni


# ============================================================
# 方案 4：手写 next_int 指针扫描  ——  极限省内存 + PyPy 利器
#   速度：★★★（CPython，慢）/ ★★★★★（PyPy，JIT 编译后很快）
#   内存：仅原始输入 bytes
#   适合：PyPy3 提交大输入题；CPython 下仅作内存兜底
#   坑：CPython 下 2×10^7 字符约 5~10 秒
# ============================================================
def load_manual():
    data = sys.stdin.buffer.read()
    L = len(data)
    ptr = 0

    def ni():
        nonlocal ptr
        while ptr < L and data[ptr] <= 32:
            ptr += 1
        sign = 1
        if ptr < L and data[ptr] == 45:  # '-'
            sign = -1
            ptr += 1
        num = 0
        while ptr < L and data[ptr] > 32:
            num = num * 10 + (data[ptr] - 48)
            ptr += 1
        return sign * num

    return ni


# ============================================================
# 使用示例：按需取消注释一种方案
# ============================================================
def main():

    # ---------- 选 1：readline().split() ----------
    # n, m = read_pair()
    # a = read_list()
    # for _ in range(m):
    #     l, r, x = map(int, readline().split())

    # ---------- 选 2：read().split() ----------
    # ni = load_all()
    # n = ni(); m = ni()
    # a = [ni() for _ in range(n)]
    # for _ in range(m):
    #     l = ni(); r = ni(); x = ni()

    # ---------- 选 3：re.finditer ----------
    # ni = load_re()
    # n = ni(); m = ni()
    # a = [ni() for _ in range(n)]
    # for _ in range(m):
    #     l = ni(); r = ni(); x = ni()

    # ---------- 选 4：手写 next_int ----------
    ni = load_manual()
    n = ni()
    m = ni()
    a = [ni() for _ in range(n)]
    for _ in range(m):
        l = ni()
        r = ni()
        x = ni()

    sys.stdout.write(str(sum(a)))


if __name__ == "__main__":
    main()
