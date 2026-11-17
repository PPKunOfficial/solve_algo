def dfs(used, path, n):
    if len(path) == n:
        print("".join(f"{x:5}" for x in path))
        return
    for i in range(1, n + 1):
        if not used[i]:
            used[i] = True
            path.append(i)
            dfs(used, path, n)
            path.pop()
            used[i] = False


def main():
    n = int(input())
    used = [False] * (n + 1)
    path = []
    dfs(used, path, n)


if __name__ == "__main__":
    main()
