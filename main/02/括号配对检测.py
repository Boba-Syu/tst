def fun(n):
    x = 0
    for i in n:
        if i == '(':
            x+=1
        if i == ')':
            x-=1
        if x < 0:
            break
    if x == 0:
        print('配对成功')
    else:
        print('配对不成功')

if __name__ == '__main__':
    n = input()
    fun(n)