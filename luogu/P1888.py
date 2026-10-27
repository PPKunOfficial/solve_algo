from fractions import Fraction

a, b, c = map(int, input().split())
a, b, c = sorted((a, b, c))

print(Fraction(a, c))
