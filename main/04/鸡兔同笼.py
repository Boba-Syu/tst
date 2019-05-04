def fun():
    MAX = -10000000000
    MIN = -MAX
    a = int(input())
    for i in range(0, a // 2):
        for j in range(0, a // 2):
            if i * 2 + j * 4 == a:
                if MAX < (i + j):
                    MAX = i + j
                if MIN > (i + j):
                    MIN = i + j
    if MAX == -10000000000 and MIN == 10000000000:
        print('0 0')
    else:
        print('{} {}'.format(MIN, MAX+1))


if __name__ == '__main__':
    x = int(input())
    for xx in range(0,x):
        fun()