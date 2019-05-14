def partition(a, lo, hi):
    i, j, v = lo + 1, hi, a[lo]
    while True:
        while a[i] < v:
            if i == hi:
                break
            i += 1
        while a[j] > v:
            if j == lo:
                break
            j -= 1
        if i >= j:
            break
        a[i], a[j] = a[j], a[i]
    a[lo], a[j] = a[j], a[lo]
    return j


def sort(a, lo, hi):
    if lo >= hi:
        return
    j = partition(a, lo, hi)
    sort(a, lo, j - 1)
    sort(a, j + 1, hi)


if __name__ == '__main__':
    a = [2, 1, 5, 7, 9, 0, 6, 4, 3, 8]
    print(a)
    sort(a, 0, 9)
    print(a)
