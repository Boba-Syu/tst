import math
def isPrime(n):
    for i in range(2, int(math.sqrt(n) + 1)):
        if n % i == 0:
            return False
    return True


if __name__ == '__main__':
    num = int(input())
    if isPrime(num):
        print("yes")
    else:
        print("no")
