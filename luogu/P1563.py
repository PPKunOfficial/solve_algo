import sys


def main():
    buffered = sys.stdin.read().split()
    n, m = map(int, buffered[0:2])
    people: list[tuple[int, str]] = []
    inst: list[tuple[int, int]] = []

    # 逆时针为顺序给出朝向和职业
    for i in range(2, n * 2 + 2, 2):
        people.append((int(buffered[i]), buffered[i + 1]))
    for i in range(n * 2 + 2, n * 2 + 2 + m * 2, 2):
        inst.append((int(buffered[i]), int(buffered[i + 1])))

    # 零朝圈内 一朝圈外
    # 零 左手顺时针 右手逆时针
    # 朝内 左手顺时针 对应列表逆序
    pointp = 0
    for i in range(m):
        # 指令 0 代表向左数
        now_inst = inst[i]
        # 零 朝圈内
        if people[pointp][0] == 0:
            if now_inst[0] == 0:
                move = now_inst[1] % len(people)
                pointp -= move
                if pointp < 0:
                    pointp = len(people) + pointp
            else:
                move = now_inst[1] % len(people)
                pointp += move
                pointp = pointp % len(people)
        else:
            if now_inst[0] == 1:
                move = now_inst[1] % len(people)
                pointp -= move
                if pointp < 0:
                    pointp = len(people) + pointp
            else:
                move = now_inst[1] % len(people)
                pointp += move
                pointp = pointp % len(people)
    print(people[pointp][1])
    return


if __name__ == "__main__":
    main()
