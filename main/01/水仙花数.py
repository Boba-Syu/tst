def fun(n):
    for i in range(100, n):
        a = i % 10
        b = (i % 100 - a) // 10
        c = i // 100
        if (a ** 3 + b ** 3 + c ** 3) == i:
            if i == 407:
                n = ""
            else:
                n = ", "
            print(i, end=n)


def fun2(n):
    a = n % 10
    b = (n // 10) % 10
    c = n // 100
    if a ** 3 + b ** 3 + c ** 3 == n:
        return True
    return False


if __name__ == '__main__':
    # n = int(input())
    # x = fun2(n)
    # print(x)
    fun(999)
