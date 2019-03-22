def fun(n):
    if n == 1 or n == 2:
        return 1
    return fun(n - 1) + fun(n - 2)


def fun2(n):
    x = 1
    y = 1
    m = 1
    for i in range(2, n):
        m = x + y
        x = y
        y = m
    return m

def main():
    n = int(input('请输入初始数字: '))
    print("递归求解:", fun(n))
    print("递推求解:", fun2(n))


if __name__ == '__main__':
    main()
