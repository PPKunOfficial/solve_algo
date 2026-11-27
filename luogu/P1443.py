import sys
from collections import deque

HORSE_DX = [-2, -2, 2, 2, 1, -1, 1, -1]
HORSE_DY = [-1, 1, -1, 1, 2, -2, -2, 2]


def main():
    n, m, x, y = map(int, sys.stdin.buffer.readline().split())
    dist = [[-1 for _ in range(410)] for _ in range(410)]

    q = deque()
    dist[x][y] = 0
    q.append((x, y))

    while len(q):
        cx, cy = q.popleft()

        for i in range(8):
            nx, ny = cx + HORSE_DX[i], cy + HORSE_DY[i]

            if nx < 1 or nx > n or ny < 1 or ny > m:
                continue

            if dist[nx][ny] != -1:
                continue

            dist[nx][ny] = dist[cx][cy] + 1
            q.append((nx, ny))

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            print(dist[i][j], end=" ")
        print()


main()
