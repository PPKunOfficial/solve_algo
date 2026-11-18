import random

random.seed(20241118)

n = 10**6

with open("input.txt", "w") as f:
    f.write("1\n")
    f.write(str(n) + "\n")

    a = []
    for i in range(n):
        if i % 97 == 0:
            x = 1
        elif i % 89 == 0:
            x = 10**9
        elif i % 13 == 0:
            x = (i * 1000003) % (10**9) + 1
        else:
            x = random.randint(1, 10**9)
        a.append(str(x))

    f.write(" ".join(a) + "\n")

print("input.txt generated")
