if __name__ == '__main__':
    ls = eval(input())
    for i in range(0, len(ls)):
        for j in range(i, len(ls) - 1):
            if ls[j] == 0:
                ls[j], ls[j + 1] = ls[j + 1], ls[j]
    print(ls)
