if __name__ == '__main__':
    a = int(input())
    for i in range(2, a + 1):
        for j in range(2, a + 1):
            for k in range(j, a + 1):
                for l in range(k, a + 1):
                    if i ** 3 == j ** 3 + k ** 3 + l ** 3:
                        print('Cube = {0},Tripe = ({1},{2},{3})'.format(i, j, k, l))
