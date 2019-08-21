def _f1(n, l, r):
    if l == r:
        return l
    mid = (l + r + 1) // 2
    if n < mid * mid:
        return _f1(n, l, mid)
    else :
        return _f1(n, mid + 1, r)
    
def f1(n):
    return _f1(n, 1, n)

def f2(x):
    # return x % 2 + f2(x >> 1)
    return len(bin(x)[2:].replace('0', ''))

def f3(x):
    return x % 2

def _f4(n, m):
    if n == 0:
        return 0
    elif m == 0:
        return 1

    if n % m == 0:
        n = 0
    else :
        if m * m <= n:
            m += 1
        else:
            m = 0
    return _f4(n, m)

def f4(n):
    if n <= 2:
        return n - 1
    return _f4(n, 2)

# f3(f2([2,3,4,5]))
# [1, 1, 1, 1]

# 963 4396 6666 1999 3141

dst = [963, 4396, 6666, 1999, 3141]
xs = [x * x for x in dst]
print(xs)
# 927369, 19324816, 44435556, 3996001, 9865881

sum = 0
for i in range(1, 10001):
    sum += f4(i)
print(sum) # 1229