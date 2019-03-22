import datetime
from datetime import time

import math


def GetNowTime():
    return datetime.datetime.now().strftime('%H:%M:%S.%f')


def fun1(f, nn):  # 求完数
    zz = 0
    print("完数: ")
    f.write("\n完数: \n")
    for n in range(1, nn):
        sum = 1
        ms = int(math.sqrt(n)) + 1
        # print(ms)
        # print(n, ": ")
        for i in range(2, ms):
            if n % i == 0:
                # print("\t",i)
                sum += i
                sum += n // i
            # print(sum, n)
        if sum == n:
            f.write(str(n) + "\t")
            print(n)
            zz += 1
    print("完数共", zz, "个")
    f.write("\n完数共"+str(zz)+ "个\n")


def fun2(f):  # 水仙花数
    zz = 0
    print("水仙花数: ")
    f.write("\n水仙花数: \n")
    n = 999
    for i in range(100, n):
        a = i % 10
        b = (i % 100 - a) // 10
        c = i // 100
        if (a ** 3 + b ** 3 + c ** 3) == i:
            f.write(str(i) + "\t")
            print(i)
            zz += 1
    print("水仙花数共", zz, "个")
    f.write("\n水仙花数共"+str(zz)+ "个\n")


def fun3(f, nn):  # 素数
    zz = 0
    print("素数: ")
    f.write("\n素数: \n")
    for n in range(2, nn):
        ms = int(math.sqrt(n)) + 1
        tmp = 1
        for i in range(2, ms):
            if n % i == 0:
                tmp = 0
                break
        if tmp == 1:
            f.write(str(n) + "\t")
            print(n)
            zz += 1
    print("素数共", zz, "个")
    f.write("\n素数共"+str(zz)+ "个\n")


def fun4(f, nn):  # 回文数
    zz = 0
    print("回文数:")
    f.write("\n回文数: \n")
    for n in range(10, nn):
        # print(n, n, n)
        a = n % 10
        m = n // 10
        while (m != 0):
            a = a * 10 + m % 10
            m = m // 10
        # print(n, a)
        if a == n:
            f.write(str(n) + "\t")
            print(n)
            zz += 1
    print("回文数共", zz, "个")
    f.write("\n回文数共"+str(zz)+ "个\n")


if __name__ == '__main__':
    n = 1000000
    f = open('text.txt', 'w', encoding="UTF-8")
    print("当前时间: " + GetNowTime())
    f.write("\n\n当前时间: " + str(GetNowTime()) + "\n")
    fun1(f, n)
    print("当前时间: " + GetNowTime())
    f.write("\n\n当前时间: " + str(GetNowTime()) + "\n")
    fun2(f)
    print("当前时间: " + GetNowTime())
    f.write("\n\n当前时间: " + str(GetNowTime()) + "\n")
    fun3(f, n)
    print("当前时间: " + GetNowTime())
    f.write("\n\n当前时间: " + str(GetNowTime()) + "\n")
    fun4(f, n)
    print("当前时间: " + GetNowTime())
    f.write("\n\n当前时间: " + str(GetNowTime()) + "\n")
    print("end.")
    f.write("end.")
    f.close()
