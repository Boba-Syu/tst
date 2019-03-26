import turtle as t


def init():
    t.setup(960, 540)
    t.speed(0)
    t.penup()
    # t.fd(-960 // 2 + 10)
    t.setx(-300)
    t.sety(-135)

    t.pendown()
    t.pensize(10)
    t.pencolor('red')


def init2():
    t.setup(960, 540)
    t.speed(0)
    t.penup()
    # t.fd(-960 // 2 + 10)
    t.setx(240)
    t.sety(-135)

    t.pendown()
    t.pensize(10)
    t.pencolor('red')


def draw(a):
    t.speed(1)
    t.seth(-40 + 45 * a)
    for i in range(0, 1):
        t.circle(40, 80)
        t.circle(-40, 80)


def despise():
    t.done()


if __name__ == '__main__':
    init()
    for i in range(8):
        draw(i)

    init2()
    for i in range(8):
        draw(i)
    despise()
