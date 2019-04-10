def fun(n):
    x1 = x2 = 1
    for i in range(1, 365):
        x1 *= (1 + n * 0.001)
        x2 *= (1 - n * 0.001)

    print("%.2f, %.2f, %d" % (x1, x2, round(x1 / x2)))


def fun2(n):
    up = 1.0 * pow(1 + n * 0.001, 365)
    down = 1.0 * pow(1 - n * 0.001, 365)
    print("{:.2f}, {:.2f}, {}".format(up, down, round(up / down)))


def fun3(n):
    up = 1.0 * ((1 + n * 0.001) ** 365)
    down = 1.0 * ((1 - n * 0.001) ** 365)
    print("{:.2f}, {:.2f}, {}".format(up, down, round(up / down)))


if __name__ == '__main__':
    n = eval(input(""))
    fun(n)
    fun2(n)
    fun3(n)
