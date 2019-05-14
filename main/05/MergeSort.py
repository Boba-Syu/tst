def merge(a, lo, mid, hi):
    i, j = lo, mid + 1
    aux = []
    for x in a:
        aux.append(x)
    k = lo
    while k <= hi:
        if i > mid:
            a[k] = aux[j]
            j += 1
            break
        elif j > hi:
            a[k] = aux[i]
            i += 1
            break
        elif aux[i] < aux[j]:
            a[k] = aux[i]
            i += 1
        else:
            a[k] = aux[j]
            j += 1
        k += 1


def top_down_sort(a, lo, hi):
    if lo >= hi:
        return
    mid = (lo + hi) // 2
    top_down_sort(a, lo, mid)
    top_down_sort(a, mid + 1, hi)
    merge(a, lo, mid, hi)


if __name__ == '__main__':
    a = [2, 1, 5, 7, 9, 0, 6, 4, 3, 8]
    print(a)
    top_down_sort(a, 0, 9)
    print(a)
