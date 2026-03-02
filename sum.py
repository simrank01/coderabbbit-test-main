from functools import reduce
arr = [12, 3, 4, 15]
sum = reduce(lambda a, b: a + b, arr)
print('Sum:', sum)
