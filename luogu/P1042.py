import sys


def calc(s: str, target: int):
    a = b = 0
    res = []

    for ch in s:
        if ch == "W":
            a += 1
        elif ch == "L":
            b += 1

        if (a >= target or b >= target) and abs(a - b) >= 2:
            res.append((a, b))
            a = b = 0

    res.append((a, b))
    return res


def main():
    data = sys.stdin.read()

    s = []
    for ch in data:
        if ch == "E":
            break
        if ch == "W" or ch == "L":
            s.append(ch)
    s = "".join(s)

    # 11 分制
    for a, b in calc(s, 11):
        print(f"{a}:{b}")

    print()

    # 21 分制
    for a, b in calc(s, 21):
        print(f"{a}:{b}")


if __name__ == "__main__":
    main()
