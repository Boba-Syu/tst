if __name__ == '__main__':
    a = input()
    b = a[0]
    a = float(a[1:a.__len__()])
    if b in ['c', 'C']:
        a = a * 1.8 + 32
        print('F%.2f' % a)
    else:
        a = (a - 32) / 1.8
        print('C%.2f' % a)
