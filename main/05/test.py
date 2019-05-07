def add(a):
    x = ""
    for i in a:
        x += i
    print(x)
    pass


if __name__ == '__main__':
    a = ((1, 2), (3, 4), (6, 7), (8, 9), (10, 5),)
    for x, y in a:
        print(x, y)
    b = [1, 2, 4]
    for i in b:
        print(i)
    x = ['asd', 'fgh', 'jkl']
    add(x)
