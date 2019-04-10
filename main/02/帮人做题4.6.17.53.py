import turtle as t
import math as m


def can_T(a, b, ac, bc, xo, ai, bi, llen1, llen2, lo, orwrite):
    p = (a, b)
    l1 = llen1;
    l2 = llen2
    t.speed(30);
    t.pensize(0)
    t.up()
    t.seth(xo)
    t.goto(a, b)
    t.down()
    if ai == 1:
        t.pencolor(ac)
        t.fd(l1)
        t.fd(-l1 * 2)
        t.fd(l1)
    if bi == 1:
        t.lt(lo)
    if bi == 1:
        t.pencolor(bc)
        t.fd(l2)
        t.fd(-l2 * 2)
        t.fd(l2)
        t.rt(lo)
    if orwrite > 0:
        t.pencolor(ac)
        t.write(p)
    t.up()
    return p


def fant(fant, fx, fy, a, b, k):
    t.pensize(1)
    fa = fant
    l = b - a;
    a11 = a;
    a12 = b
    l2 = (a + b) / 2
    t.up()
    n = int(k) + 1
    k = l / n
    fa = fant
    x = l2
    y1 = eval(fa)
    y2 = y1
    t.pencolor('red')
    xi = [a]
    for i in range(1, n + 1):
        xi += [a + i * k]
    for i in range(n + 1):
        x = xi[i]
        y = eval(fa)
        y0 = fy * (y - y1)
        e = (x - l2) * fx
        x0 = e
        t.goto(x0, y0)
        t.down()
        if i == 0:
            a21 = x0;
            b21 = y0
            b11 = y
        if i == n:
            b12 = y
    t.up()
    return [a21, b21, x0, y0, 0, 0, a11, b11, a12, b12, l2, y2]  # 12个


def kedu(a, b, lr, lc, f, k, ox, pc, ls, orfc):
    ls = ls + 1;
    lr = lr * f
    t.up();
    t.speed(30)
    p = (a, b)
    t.goto(p)
    n = 10 * int(k + 1)
    lri = lr / n
    li = [-lr]
    for i in range(1, 2 * n + 1):
        li += [-lr + i * lri]
    t.seth(ox)
    t.fd(-lr)
    for i in range(2 * n + 1):
        if i == 0:
            t.down()
        t.pencolor(pc)
        t.lt(90)
        fc = 1
        if i % 5 == 0:
            t.pensize(ls + 1)
            fc = fc * 1.25
        if i % 10 == 0:
            t.pensize(ls + 2)
            fc = fc * 1.5
            if orfc == 0:
                f = 1
            ai = round((i * lri - lr) / f, 2)
            t.dot(2.5, pc)
            t.fd(-3 * lc * fc)
            t.write(' ' + str(ai))
            t.fd(3 * lc * fc)
        t.fd(lc * fc)
        t.fd(-lc * 2 * fc)
        t.fd(lc * fc)
        t.pensize(ls)
        t.rt(90)
        if i < 2 * n:
            t.fd(lri)
        if i == n - 1:
            t.dot(5, pc)
            t.write('  0')
        if i == 0:
            t.down()
    t.up()
    t.goto(p)
    return li


def main(y):
    t.setup(1000, 800, 300, 0)
    can_T(0, 0, 'white', 'white', 0, 1, 1, 1000, 1000, 90, 0)
    k = 100  # 视图放大倍数
    t.bgcolor('grey')
    val = fant(y[3], k, k, 0.01, 3, 250)
    can_T(-val[10] * k, -val[11] * k, 'blue', 'blue', 0, 1, 1, 1000, 1000, 90, 0)
    li = kedu(-val[10] * k, -val[11] * k, 4, 3, k, 1, 0, 'blue', 0, 1)
    kedu(-val[10] * k, -val[11] * k, 4, 3, k, 1, 90, 'blue', 0, 1)
    t.goto(200, 200)
    t.write('y=' + y[2] + '   [' + str(val[6]) + ',' + str(val[8]) + ']', font=('微软雅黑', 20, 'normal'))
    print(li)
    t.done()


if __name__ == '__main__':
    y = ['lg|x|-cos x', 'm.log10(abs(x))-m.cos(x)', 'sin(x)', 'm.sin(x)']
    main(y)
