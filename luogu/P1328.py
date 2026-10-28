from enum import Enum
from re import L
import sys


class GuessE(Enum):
    JD = 0
    ST = 1
    B = 2
    XYR = 3
    SBK = 4


class GuessStatus(Enum):
    WIN = 1
    LOSE = 2
    DRAW = 3


def judge_by_rules(甲: GuessE, 乙: GuessE) -> GuessStatus:
    if 甲 == 乙:
        return GuessStatus.DRAW

    # 罗列所有“甲赢”的组合（根据星战规则）
    win_combinations = {
        (GuessE.JD, GuessE.B),  # 剪刀剪布
        (GuessE.JD, GuessE.XYR),  # 剪刀断蜥蜴人
        (GuessE.ST, GuessE.JD),  # 石头砸剪刀
        (GuessE.ST, GuessE.XYR),  # 石头砸蜥蜴人
        (GuessE.B, GuessE.ST),  # 布包石头
        (GuessE.B, GuessE.SBK),  # 布盖斯波克
        (GuessE.XYR, GuessE.B),  # 蜥蜴人吃布
        (GuessE.XYR, GuessE.SBK),  # 蜥蜴人毒斯波克
        (GuessE.SBK, GuessE.JD),  # 斯波克碎剪刀
        (GuessE.SBK, GuessE.ST),  # 斯波克化石头
    }

    if (甲, 乙) in win_combinations:
        return GuessStatus.WIN
    else:
        return GuessStatus.LOSE


def main():
    buffered = list(map(int, sys.stdin.read().split()))
    n, na, nb = map(int, buffered[0:3])
    a, b = buffered[3 : 3 + na], buffered[3 + na : 3 + na + nb]
    ass, bss = 0, 0
    for i in range(n):
        now_a, now_b = GuessE(a[i % len(a)]), GuessE(b[i % len(b)])
        r = judge_by_rules(now_a, now_b)
        if r is GuessStatus.WIN:
            ass += 1
        elif r is GuessStatus.LOSE:
            bss += 1
        else:
            continue
    print(ass, bss)
    return


if __name__ == "__main__":
    main()
