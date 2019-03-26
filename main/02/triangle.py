import turtle as t

if __name__ == '__main__':
    t.speed(0)
    t.pensize(2)
    t.bgcolor('black')
    colors = ['red', 'yellow', 'blue']
    for i in range(200):
        t.pencolor(colors[i%3])
        t.fd(i)
        t.left(120)
    t.done()
