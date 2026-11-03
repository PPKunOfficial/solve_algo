import sys


def calc(l):
    tot_time = 0
    tasks = []
    etime = 0
    nl = l
    bef = len(nl)
    for i in range(bef):
        n = nl.pop()
        tasks.append(n)
        if len(tasks) == 2:
            tot_time += max(tasks[0], tasks[1]) - etime
            etime = max(tasks[0], tasks[1]) - min(tasks[0], tasks[1])
            tasks = []
            continue
        if i == bef - 1 and len(tasks) == 1:
            tot_time += tasks[0] - etime
            etime = 0
            tasks = []
    return tot_time


def main():
    s = list(map(int, sys.stdin.readline().split()))
    a = list(map(int, sys.stdin.readline().split()))
    b = list(map(int, sys.stdin.readline().split()))
    c = list(map(int, sys.stdin.readline().split()))
    d = list(map(int, sys.stdin.readline().split()))
    a.sort()
    b.sort()
    c.sort()
    d.sort()

    tot_time = 0

    tot_time += calc(a)
    tot_time += calc(b)
    tot_time += calc(c)
    tot_time += calc(d)

    print(tot_time)
    return


if __name__ == "__main__":
    main()
