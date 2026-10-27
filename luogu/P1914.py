n = int(input()) % 26
s = input()
res = ''.join(
    # 先统一挪回以'a'为0开头，做成0-25循环
    # 后面再通过取模26，得到在下一新循环中的位置
    # 然后+ord('a')挪回以'a'开头
    chr((ord(c) - ord('a') + n) % (ord('z') - ord('a') + 1) + ord('a'))
    for c in s
)
print(res)
