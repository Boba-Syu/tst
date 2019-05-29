n = eval(input(""))
if n > 80000:
    sum = (n - 3500) * 0.45
elif n > 55000:
    sum = (n - 3500) * 0.35
elif n > 35000:
    sum = (n - 3500) * 0.3
elif n > 9000:
    sum = (n - 3500) * 0.25
elif n > 4500:
    sum = (n - 3500) * 0.1
    if sum < 0:
        sum = 0
else:
    sum = 0
print(int(sum))