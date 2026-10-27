# 维护单调栈很重要！


class SubStack:
    def __init__(self) -> None:
        self.stack: list[int] = []

    def push(self, n: int, k: int = 0) -> int:
        """
        尝试弹出栈中所有大于 n 的栈顶元素，最多弹 k 次。
        然后把 n 入栈，返回实际弹出的次数。
        """
        popped = 0
        # 弹出次数小于可弹出次数 栈非空 栈顶大于待入
        while popped < k and self.stack and self.stack[-1] > n:
            self.stack.pop()
            popped += 1
        self.stack.append(n)
        return popped

    def pop(self) -> bool:
        """弹出成功返回 True，失败返回 False"""
        if self.stack:
            self.stack.pop()
            return True
        return False

    def get(self) -> list[int]:
        return self.stack


def main() -> None:
    n = input().strip()
    k = int(input())

    s = SubStack()
    for ch in n:
        popped = s.push(int(ch), k)
        k -= popped

    if k > 0:
        del s.get()[-k:]

    result = "".join(map(str, s.get())).lstrip("0") or "0"
    print(result)


if __name__ == "__main__":
    main()
