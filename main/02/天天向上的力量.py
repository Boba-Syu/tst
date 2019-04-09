def fun(n):
    x1 = x2 = 1
    for i in range(1, 365):
        x1 *= (1 + n * 0.001)
        x2 *= (1 - n * 0.001)

    print("%.2f, %.2f, %d" % (x1, x2, x1 // x2))


if __name__ == '__main__':
    while True:
        try:
            n = int(input(""))
            fun(n)
        except:
            break
