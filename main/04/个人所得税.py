if __name__ == '__main__':
    x = 0
    a = (int(input()) - 3500)//100
    if 0 < a and a <= 15:
        x = 3
    elif 15 < a and a <= 45:
        x = 10
    elif 45 < a and a <= 90:
        x = 20
    elif 90 < a and a <= 350:
        x = 25
    elif 350 < a and a <= 550:
        x = 30
    elif 550 < a and a <= 800:
        x = 35
    elif x > 800:
        x = 45
    print(x * a)
