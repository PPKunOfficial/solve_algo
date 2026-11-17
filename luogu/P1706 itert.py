print(
    "\n".join(
        "".join(f"{x:5}" for x in i)
        for i in __import__("itertools").permutations(range(1, int(input()) + 1))
    )
)
