def fun(x):
    n = ""
    for i in x:
        if i != " ":
            i = chr((ord(i) - 97 + 3) % 26 + 97)
            n = n + i
        elif i == " ":
            n = n + " "
    print(n, end='')


if __name__ == '__main__':
    while True:
        try:
            n = input("")
            fun(n)
        except:
            break
