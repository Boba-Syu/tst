if __name__ == '__main__':
    a = input()
    b = a[-1]
    if b not in ['$', '￥']:
        b = a[-3: a.__len__()]
        a = float(a[0:-3])
    else:
        a = float(a[0:-1])
    if b == '$':
        # print(1)
        a = a * 6.78
        print("%.2f￥" % a)
    elif b == '￥':
        # print(2)
        a = a / 6.78
        print("%.2f$" % a)
    elif b in ['usd', 'USD']:
        # print(3)
        a = a * 6.78
        print("%.2fRMB" % a)
    else:
        # print(4)
        a = a / 6.78
        print("%.2fUSD" % a)
