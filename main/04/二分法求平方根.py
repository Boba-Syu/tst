import math


def sqrt_binary(num):
    x = math.sqrt(num)
    y = num / 2.0
    low = 0.0
    up = num * 1.0
    count = 1
    while abs(y - x) > 0.000000001:
        count += 1
        if (y * y > num):
            up = y
            y = (y + low) / 2
        else:
            low = y
            y = (up + y) / 2
    return y


def sqrt_newton(num):
    x = math.sqrt(num)
    y = num / 2.0
    count = 1
    while abs(y - x) > 0.00000001:
        print
        count, y
        count += 1
        y = ((y * 1.0) + (1.0 * num) / y) / 2.0000
    return y


if __name__ == '__main__':
    n = float(input())
    print(sqrt_binary(n))
    #print(sqrt_newton(n))
    print(math.sqrt(n))
