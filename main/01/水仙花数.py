def fun(n):
    for i in range(100, n):
        a = i % 10
        b = (i % 100 - a) // 10
        c = i // 100
        if (a ** 3 + b ** 3 + c ** 3) == i:
            print(i,end=" ")


if __name__ == '__main__':
    print("水仙花数有: ",end="")
    fun(999)
