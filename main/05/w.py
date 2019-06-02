a = '00000010100101000001111010011100'
print('a\t', a)
b = bin(int(a, 2))
c = b[2:]
nc = 32 - len(c)
c = '0'*nc + c
print('b\t', b)
print('b\t', c)
print('-c\t', c[::-1])
d = int(c[::-1], 2)
print('d\t', d)
