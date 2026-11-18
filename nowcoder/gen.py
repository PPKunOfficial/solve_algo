import random

random.seed(1)
with open("/Users/pp/projects/solve_q/input.txt", "w") as f:
    f.write("3\n")
    for _ in range(3):
        n = random.randint(1, 3000)
        f.write(str(n) + "\n")
        f.write(" ".join(str(random.randint(1, 10**9)) for _ in range(n)) + "\n")
