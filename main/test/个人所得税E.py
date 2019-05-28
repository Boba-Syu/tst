def fun(s):
    if s <= 3500:
        return 0
    elif 3500 < s <= 4500:
        return int(s*0.1)
    elif 4500 < s <= 9000:
        return int((s-3500) * 0.2)
    elif 9000 < s <= 35000:
        return int((s-3500) * 0.25)
    elif 35000 < s <= 55000:
        return int((s-3500) * 0.30)
    elif 55000 < s <= 80000:
        return int((s-3500) * 0.35)
    elif 80000 < s:
        return int((s-3500) * 0.45)

if __name__ == '__main__':
    s = int(input())
    print(fun(s))