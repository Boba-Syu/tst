def fun(x):
    n = ""
    for i in x:
        if i.isalpha():
            if 'a' <= i <= 'z':
                i = chr((ord(i) - ord('a') + 3) % 26 + 97).lower()
            else:
                i = chr((ord(i) - ord('A') + 3) % 26 + 97).upper()
        n = n + i
    print(n, end='')


if __name__ == '__main__':
    str = input()
    fun(str)
