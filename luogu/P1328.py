from enum import Enum
from re import L


class GuessE(Enum):
    JD = 1
    ST = 2
    B = 3
    XYR = 4
    SBK = 5


class GuessStatus(Enum):
    WIN = 1
    LOSE = 2
    DRAW = 3


guess_label = [
    [
        GuessStatus.DRAW,
        GuessStatus.LOSE,
        GuessStatus.WIN,
        GuessStatus.WIN,
        GuessStatus.LOSE,
    ],
    [
        GuessStatus.WIN,
        GuessStatus.DRAW,
        GuessStatus.LOSE,
        GuessStatus.WIN,
        GuessStatus.LOSE,
    ],
    [
        GuessStatus.LOSE,
        GuessStatus.WIN,
        GuessStatus.DRAW,
        GuessStatus.LOSE,
        GuessStatus.WIN,
    ],
    [
        GuessStatus.LOSE,
        GuessStatus.LOSE,
        GuessStatus.WIN,
        GuessStatus.DRAW,
        GuessStatus.WIN,
    ],
]


def guess(a: GuessE, b: GuessE) -> GuessStatus:
    return GuessStatus.LOSE


def main():
    return


if __name__ == "__main__":
    main()
