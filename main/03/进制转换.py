def getSign(a):
    if a < 0:
        return '-'
    else:
        return ''


def getString(absA, b):
    str = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    x = absA // b
    y = absA % b
    n = str[y]
    while x != 0:
        y = x % b
        x = x // b
        n += str[y]
    return n[::-1]


if __name__ == '__main__':
    a = int(input())
    b = int(input())
    mark = getSign(a)
    bitString = getString(abs(a), b)
    print(mark + bitString)
